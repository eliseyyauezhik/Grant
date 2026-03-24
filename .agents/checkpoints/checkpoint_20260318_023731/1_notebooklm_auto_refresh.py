import argparse
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from itertools import count
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import websocket
except ImportError as error:  # pragma: no cover
    raise SystemExit(
        "Module 'websocket' is missing. Run the script with "
        r"C:\Users\Admin\.gemini\antigravity\venv\Scripts\python.exe"
    ) from error


REQUEST_IDS = count(1)


def fetch_json(url: str, method: str = "GET") -> Any:
    request = urllib.request.Request(url, method=method)
    with urllib.request.urlopen(request, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def ensure_target(debug_port: int, target_url: str) -> dict[str, Any]:
    targets = fetch_json(f"http://127.0.0.1:{debug_port}/json")
    for target in targets:
        current_url = str(target.get("url") or "")
        if "webSocketDebuggerUrl" in target and "notebooklm.google.com" in current_url:
            return target
    create_url = (
        f"http://127.0.0.1:{debug_port}/json/new?"
        f"{urllib.parse.quote(target_url, safe='')}"
    )
    try:
        created = fetch_json(create_url, method="PUT")
    except urllib.error.HTTPError as error:
        if error.code != 405:
            raise
        created = fetch_json(create_url, method="GET")
    if isinstance(created, list):
        return created[0]
    return created


def send_cmd(
    ws: websocket.WebSocket,
    method: str,
    params: dict[str, Any] | None = None,
    msg_id: int | None = None,
) -> int:
    request_id = msg_id or next(REQUEST_IDS)
    payload: dict[str, Any] = {"id": request_id, "method": method}
    if params:
        payload["params"] = params
    ws.send(json.dumps(payload))
    return request_id


def wait_for_response(ws: websocket.WebSocket, msg_id: int, timeout: int = 10) -> dict[str, Any]:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            raw_message = ws.recv()
        except websocket.WebSocketTimeoutException:
            continue
        message = json.loads(raw_message)
        if message.get("id") == msg_id:
            return message
    raise TimeoutError("Timed out waiting for Chrome DevTools response")


def get_page_html(ws: websocket.WebSocket) -> str:
    request_id = send_cmd(
        ws,
        "Runtime.evaluate",
        {
            "expression": "document.documentElement.outerHTML",
            "returnByValue": True,
        },
    )
    response = wait_for_response(ws, request_id, timeout=10)
    return str(response.get("result", {}).get("result", {}).get("value") or "")


def wait_for_batchexecute(ws: websocket.WebSocket, timeout: int) -> tuple[str, str]:
    deadline = time.time() + timeout
    requests: dict[str, tuple[str, str]] = {}
    headers_by_request: dict[str, dict[str, str]] = {}
    while time.time() < deadline:
        try:
            raw_message = ws.recv()
        except websocket.WebSocketTimeoutException:
            continue
        message = json.loads(raw_message)
        method = message.get("method")
        params = message.get("params", {})
        request_id = str(params.get("requestId") or "")

        if method == "Network.requestWillBeSent":
            request = params.get("request", {})
            url = str(request.get("url") or "")
            post_data = str(request.get("postData") or "")
            if "batchexecute" in url and "at=" in post_data:
                requests[request_id] = (url, post_data)
        elif method == "Network.requestWillBeSentExtraInfo" and request_id:
            headers = params.get("headers", {})
            normalized_headers = {str(key).lower(): str(value) for key, value in headers.items()}
            headers_by_request[request_id] = normalized_headers

        if request_id and request_id in requests and request_id in headers_by_request:
            url, post_data = requests[request_id]
            header_map = headers_by_request[request_id]
            cookie_header = header_map.get("cookie", "")
            return url, post_data, cookie_header, header_map

    raise TimeoutError("Timed out waiting for NotebookLM batchexecute request")


def extract_tokens_from_html(html: str) -> tuple[str | None, str | None, str | None]:
    csrf_match = re.search(r'"SNlM0e":"([^"]+)"', html)
    session_match = re.search(r'"FdrFJe":"([^"]+)"', html)
    build_match = re.search(r'"cfb2h":"([^"]+)"', html)
    csrf_token = csrf_match.group(1) if csrf_match else None
    session_id = session_match.group(1) if session_match else None
    build_label = build_match.group(1) if build_match else None
    return csrf_token, session_id, build_label


def extract_token(post_data: str) -> str:
    parsed = urllib.parse.parse_qs(post_data, keep_blank_values=True)
    token = parsed.get("at", [None])[0]
    if token:
        return token
    raise ValueError("Parameter 'at' was not found in batchexecute payload")


def parse_cookie_header(cookie_header: str) -> dict[str, str]:
    cookies: dict[str, str] = {}
    for part in cookie_header.split(";"):
        item = part.strip()
        if not item or "=" not in item:
            continue
        name, value = item.split("=", 1)
        cookies[name] = value
    return cookies


def select_request_headers(headers: dict[str, str]) -> dict[str, str]:
    keep = {
        "accept-language",
        "priority",
        "sec-ch-ua",
        "sec-ch-ua-arch",
        "sec-ch-ua-bitness",
        "sec-ch-ua-form-factors",
        "sec-ch-ua-full-version",
        "sec-ch-ua-full-version-list",
        "sec-ch-ua-mobile",
        "sec-ch-ua-model",
        "sec-ch-ua-platform",
        "sec-ch-ua-platform-version",
        "sec-ch-ua-wow64",
        "sec-fetch-dest",
        "sec-fetch-mode",
        "sec-fetch-site",
        "user-agent",
        "x-browser-channel",
        "x-browser-copyright",
        "x-browser-validation",
        "x-browser-year",
        "x-client-data",
    }
    return {key: value for key, value in headers.items() if key in keep}


def extract_query_params(url: str) -> tuple[str | None, str | None]:
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    session_id = query.get("f.sid", [None])[0]
    build_label = query.get("bl", [None])[0]
    return session_id, build_label


def extract_cookies(ws: websocket.WebSocket) -> dict[str, str]:
    request_id = send_cmd(ws, "Network.getAllCookies")
    response = wait_for_response(ws, request_id, timeout=10)
    cookie_list = response.get("result", {}).get("cookies", [])
    cookies: dict[str, str] = {}
    for cookie in cookie_list:
        domain = str(cookie.get("domain", "")).lstrip(".")
        if not (
            domain.endswith("google.com")
            or domain.endswith("notebooklm.google.com")
            or domain.endswith("googleusercontent.com")
        ):
            continue
        name = cookie.get("name")
        value = cookie.get("value")
        if name and value:
            cookies[str(name)] = str(value)
    return cookies


def update_storage(
    storage_root: Path,
    cookies: dict[str, str],
    csrf_token: str,
    session_id: str | None,
    build_label: str | None,
    request_headers: dict[str, str] | None = None,
) -> None:
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
    if request_headers:
        auth_data["request_headers"] = request_headers
    auth_path.write_text(json.dumps(auth_data, indent=2, ensure_ascii=False), encoding="utf-8")

    profile_dir = storage_root / "profiles" / "default"
    profile_dir.mkdir(parents=True, exist_ok=True)
    (profile_dir / "cookies.json").write_text(
        json.dumps(cookies, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    metadata_path = profile_dir / "metadata.json"
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    else:
        metadata = {}

    metadata["csrf_token"] = csrf_token
    metadata["session_id"] = session_id
    if build_label:
        metadata["build_label"] = build_label
    if request_headers:
        metadata["request_headers"] = request_headers
    metadata["last_validated"] = datetime.now(timezone.utc).isoformat()
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Refresh NotebookLM auth from Chrome DevTools.")
    parser.add_argument("--debug-port", type=int, default=9222, help="Chrome remote debugging port.")
    parser.add_argument(
        "--target-url",
        default="https://notebooklm.google.com/",
        help="NotebookLM URL to open or reload before capture.",
    )
    parser.add_argument(
        "--storage-root",
        default=r"C:\Users\Admin\.notebooklm-mcp-cli",
        help="NotebookLM CLI storage root.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="How long to wait for a NotebookLM batchexecute request, in seconds.",
    )
    args = parser.parse_args()

    target = ensure_target(args.debug_port, args.target_url)
    websocket_url = target.get("webSocketDebuggerUrl")
    if not websocket_url:
        raise SystemExit("Chrome DevTools target is missing webSocketDebuggerUrl")

    ws = websocket.create_connection(websocket_url, timeout=5, suppress_origin=True)
    ws.settimeout(1)
    try:
        send_cmd(ws, "Page.enable")
        send_cmd(ws, "Runtime.enable")
        send_cmd(ws, "Network.enable", {"maxPostDataSize": 1_048_576})
        send_cmd(ws, "Page.reload", {"ignoreCache": True})
        try:
            url, post_data, cookie_header, header_map = wait_for_batchexecute(ws, timeout=args.timeout)
            csrf_token = extract_token(post_data)
            session_id, build_label = extract_query_params(url)
            cookies = parse_cookie_header(cookie_header)
            request_headers = select_request_headers(header_map)
        except TimeoutError:
            time.sleep(2)
            html = get_page_html(ws)
            csrf_token, session_id, build_label = extract_tokens_from_html(html)
            cookies = extract_cookies(ws)
            request_headers = {}
    finally:
        ws.close()

    if not cookies:
        raise SystemExit("No eligible Google cookies were captured from Chrome")
    if not csrf_token:
        raise SystemExit("Failed to extract NotebookLM auth tokens from the active page")

    update_storage(
        Path(args.storage_root),
        cookies,
        csrf_token,
        session_id,
        build_label,
        request_headers=request_headers,
    )
    token_preview = f"{csrf_token[:8]}..." if csrf_token else "<none>"
    session_flag = "yes" if session_id else "no"
    build_flag = "yes" if build_label else "no"
    print(f"OK cookies={len(cookies)} token={token_preview} session_id={session_flag} build_label={build_flag}")


if __name__ == "__main__":
    main()
