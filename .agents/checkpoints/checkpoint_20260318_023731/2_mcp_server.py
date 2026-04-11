"""
YT_Analyzer_v1 — MCP-Compatible HTTP Server
Позволяет подключить скилл к любому мониторинг-сервису через REST API.

Запуск:
    python mcp_server.py --port 8765

Endpoints:
    POST /analyze          - Запустить анализ
    GET  /report/{id}      - Получить отчёт
    GET  /knowledge-base   - Получить базу знаний
    GET  /health           - Health check
    POST /improve          - Применить self-improvement
"""

import asyncio
import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import threading

from skill import YT_Analyzer_v1, REPORTS_DIR, KNOWLEDGE_BASE_DIR, LOGS_DIR

log = logging.getLogger("YT_MCP_Server")


class MCPHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        log.info(f"HTTP {self.address_string()} {format % args}")

    def send_json(self, data: dict, status=200):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/health":
            self.send_json({"status": "ok", "skill": "YT_Analyzer_v1", "version": "1.0.0"})

        elif path == "/knowledge-base":
            kb_path = KNOWLEDGE_BASE_DIR / "knowledge_base.json"
            if kb_path.exists():
                data = json.loads(kb_path.read_text())
                self.send_json(data)
            else:
                self.send_json({"error": "Knowledge base is empty"}, 404)

        elif path.startswith("/report/"):
            report_id = path.split("/report/")[1]
            report_path = REPORTS_DIR / f"{report_id}.json"
            if report_path.exists():
                data = json.loads(report_path.read_text())
                self.send_json(data)
            else:
                self.send_json({"error": f"Report {report_id} not found"}, 404)

        elif path == "/reports":
            reports = []
            for f in sorted(REPORTS_DIR.glob("*.json"), reverse=True)[:20]:
                try:
                    data = json.loads(f.read_text())
                    reports.append({
                        "report_id": data.get("report_id"),
                        "generated_at": data.get("generated_at"),
                        "total_videos": data.get("total_videos"),
                        "average_score": data.get("average_score"),
                        "criteria": data.get("criteria"),
                    })
                except Exception:
                    pass
            self.send_json({"reports": reports})

        else:
            self.send_json({"error": "Not found"}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length else "{}"

        try:
            payload = json.loads(body)
        except Exception:
            self.send_json({"error": "Invalid JSON"}, 400)
            return

        if path == "/analyze":
            url = payload.get("url")
            criteria = payload.get("criteria", "ИИ-агенты, автоматизация")
            min_score = payload.get("min_score", 0)
            max_videos = payload.get("max_videos", 30)

            if not url:
                self.send_json({"error": "Missing 'url' field"}, 400)
                return

            # Run in background thread
            def run_analysis():
                try:
                    report = asyncio.run(YT_Analyzer_v1(
                        url=url,
                        criteria=criteria,
                        min_score=min_score,
                        max_videos=max_videos,
                    ))
                    log.info(f"✅ Background analysis complete: {report['report_id']}")
                except Exception as e:
                    log.error(f"❌ Background analysis failed: {e}")

            thread = threading.Thread(target=run_analysis, daemon=True)
            thread.start()

            self.send_json({
                "status": "started",
                "message": f"Analysis started for: {url}",
                "poll_url": "/reports",
            })

        elif path == "/analyze/sync":
            # Synchronous version (blocks until complete)
            url = payload.get("url")
            criteria = payload.get("criteria", "ИИ-агенты, автоматизация")
            min_score = payload.get("min_score", 0)
            max_videos = payload.get("max_videos", 10)

            if not url:
                self.send_json({"error": "Missing 'url' field"}, 400)
                return

            try:
                report = asyncio.run(YT_Analyzer_v1(
                    url=url,
                    criteria=criteria,
                    min_score=min_score,
                    max_videos=max_videos,
                ))
                self.send_json(report)
            except Exception as e:
                self.send_json({"error": str(e)}, 500)

        elif path == "/improve":
            improvements_path = LOGS_DIR / "improvement_suggestions.md"
            if improvements_path.exists():
                content = improvements_path.read_text(encoding="utf-8")
                self.send_json({"improvements": content})
            else:
                self.send_json({"improvements": "No improvement suggestions yet. Run an analysis first."})

        else:
            self.send_json({"error": "Not found"}, 404)


def run_server(host="0.0.0.0", port=8765):
    server = HTTPServer((host, port), MCPHandler)
    log.info(f"""
╔══════════════════════════════════════════════╗
║  YT_Analyzer_v1 MCP Server                  ║
║  Running at: http://{host}:{port}           ║
╠══════════════════════════════════════════════╣
║  POST /analyze         → Async analysis      ║
║  POST /analyze/sync    → Sync analysis       ║
║  GET  /reports         → List all reports    ║
║  GET  /report/{{id}}    → Get specific report ║
║  GET  /knowledge-base  → Knowledge base      ║
║  GET  /health          → Health check        ║
╚══════════════════════════════════════════════╝
""")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log.info("Server stopped")


if __name__ == "__main__":
    import argparse
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args()
    run_server(args.host, args.port)
