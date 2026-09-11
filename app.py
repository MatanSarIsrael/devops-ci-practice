import os
import signal
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

from calc import add

VERSION = os.environ.get("APP_VERSION", "dev")
COMMIT = os.environ.get("APP_COMMIT", "unknown")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = b'{"status":"ok"}'
        elif self.path == "/version":
            body = f'{{"version":"{VERSION}","commit":"{COMMIT}"}}'.encode()
        elif self.path.startswith("/add"):
            body = f'{{"result":{add(2, 3)}}}'.encode()
        else:
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} {fmt % args}", flush=True)


def shutdown(signum, frame):
    print(f"received signal {signum}, shutting down", flush=True)
    sys.exit(0)


signal.signal(signal.SIGTERM, shutdown)

if __name__ == "__main__":
    server = HTTPServer(("", 8080), Handler)
    print(f"serving on 8080 version={VERSION} commit={COMMIT}", flush=True)
    server.serve_forever()

