import sys
import time
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler


class DefaultHTTPHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(("I'm alive at " + str(time.time())).encode("utf-8"))


def base_http_server_start(address="0.0.0.0", port=8080, backlog=None):
    handler = DefaultHTTPHandler
    address = (address, port)
    server = ThreadingHTTPServer(address, handler, bind_and_activate=False)
    if backlog is not None:
        server.request_queue_size = backlog
    server.server_bind()
    server.server_activate()
    server.serve_forever()


if __name__ == '__main__':
    backlog = None
    print("Starting HTTP server on port 8080")
    if len(sys.argv) > 1:
        backlog = int(sys.argv[1])
        print("Backlog set to %d" % backlog)
    else:
        print("Using default backlog")
    base_http_server_start(backlog=backlog)