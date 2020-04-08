from http.server import SimpleHTTPRequestHandler, HTTPServer

from netsec.server.socket_wrapper import LimiterIpBlocker, StaticIpBlocker


def base_http_server_start(address="0.0.0.0", port=8080, rate_limit=None, block_ip=None, backlog=None):
    handler = SimpleHTTPRequestHandler
    address = (address, port)
    server = HTTPServer(address, handler, bind_and_activate=False)

    if rate_limit is not None:
        server.socket = LimiterIpBlocker(server.socket, rate_limit)
    if block_ip is not None:
        server.socket = StaticIpBlocker(server.socket, block_set=block_ip)
    if backlog is not None:
        server.request_queue_size = backlog
    server.server_bind()
    server.server_activate()
    server.serve_forever()
