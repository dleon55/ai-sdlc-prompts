#!/usr/bin/env python3
import http.server
import socketserver
import os

PORT = 3001
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Si no es archivo existente, sirve index.html (SPA)
        if not os.path.isfile(self.path.lstrip('/')):
            self.path = '/index.html'
        return super().do_GET()

print(f"🚀 http://localhost:{PORT}/app")
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
