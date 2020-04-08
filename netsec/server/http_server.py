import random
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer, BaseHTTPRequestHandler

from netsec.server.socket_wrapper import LimiterIpBlocker, StaticIpBlocker, ClientLimit
from netsec.utils.generic import is_prime


def _e(s):
    return s.encode("utf-8")


class DefaultHTTPHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)

        if "dynamic" in self.path:
            return self._dynamic()
        elif "complex" in self.path:
            return self._complex()
        else:
            return self._static()

    def _static(self):
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'I\'m alive!<br>Why don\'t you visit this website!<br><a href="/dynamic">/dynamic</a><br><a href="/complex">/complex</a>')

    def _dynamic(self):
        self.send_header('Content-type', 'text/plain')
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(_e("I'm alive at " + str(time.time())))

    def _complex(self):
        self.send_header('Content-type', 'text/plain')
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        n = random.randint(10000000, 30000000)
        self.wfile.write(_e(("{} is " + ("" if is_prime(n) else "not ") + "a prime number").format(n)))


def base_http_server_start(address="0.0.0.0", port=8080, rate_limit=None, block_ip=None, backlog=None, max_clients=None):
    handler = DefaultHTTPHandler
    address = (address, port)
    server = ThreadingHTTPServer(address, handler, bind_and_activate=False)

    if rate_limit is not None:
        server.socket = LimiterIpBlocker(server.socket, rate_limit)
    if block_ip is not None:
        server.socket = StaticIpBlocker(server.socket, block_set=block_ip)
    if backlog is not None:
        server.request_queue_size = backlog
    if max_clients is not None:
        server.socket = ClientLimit(server.socket, max_clients)
    server.server_bind()
    server.server_activate()
    server.serve_forever()
