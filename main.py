import sys

from netsec.server.http_server import base_http_server_start

if __name__ == '__main__':
    backlog = None
    if len(sys.argv) > 1:
        backlog = int(sys.argv[1])
        print("Backlog set to %d" % backlog)
    base_http_server_start(backlog=backlog)