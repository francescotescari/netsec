import sys

from scapy.all import send, TCP, IP, RandIP, RandShort


def send_syn(destination_ip, destination_port, spoofed_ip=True, source_port=None):
    """Send a syn packet to destination socket"""
    source_port = RandShort() if source_port is None else source_port

    # 1) Build the IP packet
    ip_packet = IP()
    ip_packet.dst = destination_ip
    if spoofed_ip:
        ip_packet.src = RandIP()

    # 2) Build the TCP packet with the S flag
    tcp_packet = TCP()
    tcp_packet.sport = source_port
    tcp_packet.dport = destination_port
    tcp_packet.flags = "S"

    # 3) Send the IP/TCP packet
    return send(ip_packet / tcp_packet, verbose=0, loop=0)


def _internal_help(argv, option_fail=None, reason=None, help_function=None):
    if option_fail is not None:
        if reason is not None:
            msg = "Failed to parse option %r: %s" % (option_fail, reason)
        else:
            msg = "Missing required option %r" % option_fail
        print(msg)
    if help_function is not None:
        help_function(argv)
    exit(1)


def _parse_option(argv, argnum, apply_func=None, def_value=None, required=False, help_function=None, name=None):
    ename = argnum if name is None else name
    try:
        if len(argv) > argnum:
            return apply_func(argv[argnum]) if apply_func is not None else argv[argnum]
        else:
            if required:
                return _internal_help(argv, ename, help_function=help_function)
            return def_value
    except Exception as e:
        return _internal_help(argv, ename, e, help_function=help_function)


def _bool_val(arg):
    if arg.isnumeric():
        arg = int(arg)
        return arg != 0
    arg = arg.lower()
    if arg == "true":
        return True
    if arg == "false":
        return False
    raise ValueError("Invalid boolean value. Please use \"true\" or \"false\"")


def _help(argv):
    print("Usage  : sudo python3 %s target_ip target_port [spoof_ip:bool] [src_port:int]\n"
          "Example: sudo python3 %s 192.168.1.25 8080 true" % (argv[0], argv[0]))


if __name__ == '__main__':
    """Launch the script with "sudo python3 syn_exercise.py target_ip target_port [spoof_ip:bool] [src_port:int]" """
    target_ip = _parse_option(sys.argv, 1, None, None, help_function=_help, required=True, name="target_ip")
    target_port = _parse_option(sys.argv, 2, int, None, help_function=_help, required=True, name="target_port")
    spoof_ip = _parse_option(sys.argv, 3, _bool_val, False, help_function=_help, name="spoof_ip")
    src_port = _parse_option(sys.argv, 4, int, None, help_function=_help, name="src_port")
    send_syn(target_ip, target_port, spoofed_ip=spoof_ip, source_port=src_port)
