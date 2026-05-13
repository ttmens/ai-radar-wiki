"""Simple static HTTP server for ai-radar-wiki."""
import sys, os, traceback
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8780
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

try:
    Handler = SimpleHTTPRequestHandler
    server = HTTPServer(("127.0.0.1", PORT), Handler)
    # Write to a log file so we can see startup status
    with open(os.path.join(ROOT, "tools", "server.log"), "w", encoding="utf-8") as f:
        f.write(f"Server started on http://127.0.0.1:{PORT} from {ROOT}\n")
        f.flush()
    print(f"Serving http://127.0.0.1:{PORT} from {ROOT}", flush=True)
    server.serve_forever()
except Exception as e:
    with open(os.path.join(ROOT, "tools", "server.log"), "w", encoding="utf-8") as f:
        f.write(f"ERROR: {e}\n{traceback.format_exc()}\n")
    print(f"ERROR: {e}", flush=True)
    raise
