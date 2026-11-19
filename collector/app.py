#!/usr/bin/env python3
"""The Crisp Counter — self-hosted analytics collector (reference code).

A dependency-free HTTP endpoint that receives the five defined events from
assets/js/analytics.js as anonymous JSON lines and appends them to
events.jsonl. Designed to run anywhere a small service can run (VPS, Fly.io,
Render, a systemd unit) — GitHub Pages is static hosting and cannot run it,
which is why hosting is open question Q-06 (flag FLG-08).

Run:
    python3 collector/app.py --port 8090

Endpoints:
    POST /collect    {"event": "...", "ts": "...", "path": "...", "props": {...}}
    GET  /health     {"ok": true, "events": <count>}

Privacy defaults: no cookies, no IP logging, no user-agent storage; event
lines only, rotated after 90 days (RETENTION_DAYS).
"""
import argparse
import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
EVENTS_FILE = HERE / "events.jsonl"
RETENTION_DAYS = 90
ALLOWED_EVENTS = {
    "page_view",
    "product_link_click",
    "chooser_step",
    "article_read",
    "guide_to_compare_click",
}

VALIDATOR = [
    {"type": "impression", "src": "client-side tracker"},
    {"type": "click", "src": "client-side tracker"},
    {"type": "session", "src": "attribution model (carried ledger)"},
    {"type": "order", "src": "authorised Associates report only"},
    {"type": "refund", "src": "authorised Associates report only"},
]


def prune_old():
    if not EVENTS_FILE.exists():
        return
    cutoff = time.time() - RETENTION_DAYS * 86400
    lines = EVENTS_FILE.read_text(encoding="utf-8").splitlines()
    kept = []
    for line in lines:
        try:
            rec = json.loads(line)
            ts = rec.get("_received_epoch")
            if isinstance(ts, (int, float)) and ts < cutoff:
                continue
        except Exception:
            pass
        kept.append(line)
    EVENTS_FILE.write_text("\n".join(kept) + ("\n" if kept else ""), encoding="utf-8")


class Handler(BaseHTTPRequestHandler):
    server_version = "CrispCollector/1.0"

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path == "/health":
            count = len(EVENTS_FILE.read_text(encoding="utf-8").splitlines()) if EVENTS_FILE.exists() else 0
            body = json.dumps({"ok": True, "events": count}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._cors()
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path != "/collect":
            self.send_error(404)
            return
        try:
            length = min(int(self.headers.get("Content-Length", "0")), 8192)
            payload = json.loads(self.rfile.read(length) or b"{}")
        except Exception:
            self.send_error(400, "invalid JSON")
            return
        if payload.get("event") not in ALLOWED_EVENTS:
            self.send_error(422, "unknown event")
            return
        record = {
            "_received_epoch": time.time(),
            "_received_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "event": payload.get("event"),
            "ts": payload.get("ts"),
            "path": payload.get("path"),
            "props": payload.get("props", {}),
        }
        with EVENTS_FILE.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        prune_old()
        self.send_response(204)
        self._cors()
        self.end_headers()

    def log_message(self, fmt, *args):
        # Privacy default: no request logging (no IPs on disk).
        return


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8090)
    ap.add_argument("--bind", default="0.0.0.0")
    args = ap.parse_args()
    server = ThreadingHTTPServer((args.bind, args.port), Handler)
    print("collector listening on %s:%d -> %s" % (args.bind, args.port, EVENTS_FILE))
    server.serve_forever()


if __name__ == "__main__":
    main()
