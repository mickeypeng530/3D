"""開發用截圖接收 server:接收頁面 POST 的 dataURL,存成 shots/latest.png"""
import base64
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "shots")
os.makedirs(OUT_DIR, exist_ok=True)


class Handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length).decode("utf-8")
        name = self.path.strip("/").replace("..", "") or "latest"
        if "," in data:
            data = data.split(",", 1)[1]
        path = os.path.join(OUT_DIR, f"{name}.png")
        with open(path, "wb") as f:
            f.write(base64.b64decode(data))
        print(f"[OK] saved {path} ({length} bytes)")
        self.send_response(200)
        self._cors()
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8766
    print(f"[shot_server] listening on {port}, saving to {OUT_DIR}")
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()
