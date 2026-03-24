import argparse
import json
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:
    import websocket
except ImportError:  # pragma: no cover - helper message for runtime
    raise SystemExit(
        "Не найден модуль 'websocket'. Запускайте через venv: "
        "C:\\Users\\Admin\\.gemini\\antigravity\\venv\\Scripts\\python.exe notebooklm_auto_refresh.py"
    )


def fetch_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def ensure_target(debug_port: int, target_url: str) -> dict:
    targets = fetch_json(f"http://127.0.0.1:{debug_port}/json")
    for target in targets:
        if "webSocketDebuggerUrl" in target and "notebooklm.google.com" in (target.get("url") or ""):
            return target
    new_target = fetch_json(
        f"http://127.0.0.1:{debug_port}/json/new?{urllib.parse.quote(target_url, safe='')}"
    )
    return new_target


def send_cmd(ws, method: str, params: dict | None = None, msg_id: int | None = None) -> int:
    if msg_id is None:
        msg_id = int(time.time() * 1000)
    payload = {"id": msg_id, "method": method}
    if params:
        payload["params"] = params
    ws.send(json.dumps(payload))
    return msg_id


def wait_for_response(ws, msg_id: int, timeout: int = 10) -> dict:
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            msg = ws.recv()
        except websocket.WebSocketTimeoutException:
            continue
        data = json.loads(msg)
        if data.get("id") == msg_id:
            return data
    raise TimeoutError("Не удалось получить ответ от Chrome DevTools")


def wait_for_batchexecute(ws, timeout: int = 60) -> tuple[str, str]:
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            msg = ws.recv()
        except websocket.WebSocketTimeoutException:
            continue
        data = json.loads(msg)
        if data.get("method") != "Network.requestWillBeSent":
            continue
        request = data.get("params", {}).get("request", {})
        url = request.get("url") or ""
        post_data = request.get("postData") or ""
        if "batchexecute" not in url or "at=" not in post_data:
            continue
        return url, post_data
    raise TimeoutError("Не удалось поймать запрос batchexecute с параметром at")


def extract_token(post_data: str) -> str:
    match = re.search(r"\\bat=([^&\\s]+)", post_data)
    if not match:
        raise ValueError("Параметр at не найден в postData")
    return urllib.parse.unquote(match.group(1))


def extract_query_params(url: str) -> tuple[str | None, str | None]:
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    session_id = query.get("f.sid", [None])[0]
    build_label = query.get("bl", [None])[0]
    return session_id, build_label


def update_storage(storage_root: Path, cookies: dict, csrf_token: str, session_id: str | None, build_label: str | None) -> None:
    auth_path = storage_root / "auth.json"
    if auth_path.exists():
        auth_data = json.loads(auth_path.read_text(encoding="utf-8"))
    else:
        auth_data = {"cookies": {}, "csrf_token": None, "session_id": None}

    auth_data["cookies"] = cookies
    auth_data["csrf_token"] = csrf_token
    auth_data["session_id"] = session_id
    if build_label:
        auth_data["build_label"] = build_label

    auth_path.write_text(json.dumps(auth_data, indent=2, ensure_ascii=False), encoding="utf-8")

    profile_dir = storage_root / "profiles" / "default"
    profile_dir.mkdir(parents=True, exist_ok=True)
    (profile_dir / "cookies.json").write_text(json.dumps(cookies, indent=2, ensure_ascii=False), encoding="utf-8")

    meta_path = profile_dir / "metadata.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    else:
        meta = {}

    meta["csrf_token"] = csrf_token
    meta["session_id"] = session_id
    if build_label:
        meta["build_label"] = build_label
    meta["last_validated"] = datetime.now(timezone.utc).isoformat()

    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Автоматическое обновление NotebookLM токенов через Chrome DevTools.")
    parser.add_argument("--debug-port", type=int, default=9222, help="Порт remote debugging Chrome (по умолчанию 9222).")
    parser.add_argument(
        "--target-url",
        default="https://notebooklm.google.com/",
        help="URL NotebookLM для открытия/перезагрузки.",
    )
    parser.add_argument(
        "--storage-root",
        default=r"C:\\Users\\Admin\\.notebooklm-mcp-cli",
        help="Корень хранилища NotebookLM CLI.",
    )
    parser.add_argument("--timeout", type=int, default=60, help="Таймаут ожидания batchexecute (сек).")
    args = parser.parse_args()

    target = ensure_target(args.debug_port, args.target_url)
    ws_url = target.get("webSocketDebuggerUrl")
    if not ws_url:
        raise SystemExit("Не найден webSocketDebuggerUrl. Проверьте, что Chrome запущен с --remote-debugging-port.")

    ws = websocket.create_connection(ws_url)
    ws.settimeout(1)
    try:
        send_cmd(ws, "Network.enable", {"maxPostDataSize": 1048576})
        send_cmd(ws, "Page.enable")
        send_cmd(ws, "Runtime.evaluate", {"expression": "location.reload()", "includeCommandLineAPI": True})

        url, post_data = wait_for_batchexecute(ws, timeout=args.timeout)
        csrf_token = extract_token(post_data)
        session_id, build_label = extract_query_params(url)

        cookies_msg_id = send_cmd(ws, "Network.getAllCookies")
        cookies_resp = wait_for_response(ws, cookies_msg_id, timeout=10)
        cookie_list = cookies_resp.get("result", {}).get("cookies", [])
    finally:
        ws.close()

    cookies = {}
    for cookie in cookie_list:
        domain = cookie.get("domain", "").lstrip(".")
        if not (
            domain.endswith("google.com")
            or domain.endswith("notebooklm.google.com")
            or domain.endswith("googleusercontent.com")
        ):
            continue
        name = cookie.get("name")
        value = cookie.get("value")
        if name and value:
            cookies[name] = value

    if not cookies:
        raise SystemExit("Не удалось извлечь cookies из Chrome. Проверьте активный аккаунт.")

    update_storage(Path(args.storage_root), cookies, csrf_token, session_id, build_label)
    token_preview = f\"{csrf_token[:8]}...\" if csrf_token else \"<none>\"
    print(
        f\"OK: cookies={len(cookies)} token={token_preview} session_id={'yes' if session_id else 'no'}\"
    )


if __name__ == "__main__":
    main()
