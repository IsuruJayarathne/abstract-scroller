import http.server, socketserver, argparse, os

class BrotliHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # allow cross-origin (useful if you open the HTML elsewhere)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        if self.path.endswith(".json.br"):
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Encoding", "br")
        super().end_headers()

    # noisy logs so you can see every request path
    def log_message(self, fmt, *args):
        print(self.address_string(), "-", self.command, self.path, "-", fmt % args)

class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="data")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--host", default="127.0.0.1")
    args = ap.parse_args()
    os.chdir(args.root)
    httpd = ThreadingHTTPServer((args.host, args.port), BrotliHandler)
    print(f"Serving {os.getcwd()} at http://{args.host}:{args.port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()

if __name__ == "__main__":
    main()
