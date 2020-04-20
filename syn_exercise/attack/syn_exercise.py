import sys
from scapy.all import send, TCP, IP, RandIP, RandShort
from syn_solution import _parse_option, _bool_val


def send_syn(destination_ip, destination_port, spoofed_ip=True, source_port=None):
    """Send a syn packet to destination socket. Optionally spoof the origin ip"""
    source_port = RandShort() if source_port is None else source_port

    # Use the scapy library to send a syn packet to the destination socket
    # All the necessary classes and functions are already imported

    # 1) Build the IP packet
    ip_packet = IP()
    ip_packet.dst = destination_ip
    if spoofed_ip:
        ip_packet.src = RandIP()

    # 2) Build the TCP SYN packet
    # TODO COMPLETE THE TCP HEADER HERE
    # tcp_packet =

    # 3) Send the IP/TCP packet
    return send(ip_packet / tcp_packet, verbose=0, loop=0)


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
