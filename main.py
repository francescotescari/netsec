from netsec.server.http_server import base_http_server_start

base_http_server_start(rate_limit=(20, 5), backlog=1, max_clients=10)