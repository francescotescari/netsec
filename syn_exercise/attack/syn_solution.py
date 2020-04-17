from random import randint

from scapy.all import send, TCP, IP


def random_ip():
    """Return a random ip address."""
    return ".".join(map(str, (randint(1, 255) for _ in range(4))))


def random_private_port():
    """Return a random port number among the private ports."""
    return randint(49152, 65535)


def send_syn(destination_ip, destination_port, spoofed_ip=True):
    """Send a syn packet to destination socket. Optionally spoof the origin ip"""
    # Use the scapy library to send a syn packet to the destination socket
    # All the necessary classes and functions are already imported
    # Remember that a syn packet is a simple tcp packet with the syn flag enabled
    ip_packet = IP()
    ip_packet.dst = destination_ip
    if spoofed_ip:
        ip_packet.src = random_ip()

    tcp_packet = TCP()
    tcp_packet.sport = random_private_port()
    tcp_packet.dport = int(destination_port)
    tcp_packet.flags = "S"
    tcp_packet.seq = 0
    tcp_packet.window = 65535
    return send(ip_packet / tcp_packet, verbose=0, loop=0)
