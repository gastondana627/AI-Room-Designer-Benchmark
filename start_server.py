import http.server
import socketserver
import os
import sys

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

def run_server():
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"Serving at http://localhost:{PORT}")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 98:
            print(f"Port {PORT} already in use. Server likely already running.")
        else:
            raise e

if __name__ == "__main__":
    # Check if index.html exists
    if not os.path.exists("index.html"):
        print("index.html not found. Please run local_app.py first.")
        sys.exit(1)
    run_server()
