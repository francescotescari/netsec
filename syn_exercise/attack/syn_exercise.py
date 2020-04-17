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
    # 1) Create an IP packet with destination set to destination_ip
    # 2) If spoofed_ip is True, set the source to a random ip address
    # 3) Create a syn tcp packet (flags = "S") with destination port set to destination_port, random source port
    # 4) Send the TCP / IP packet using send


if __name__ == '__main__':
    """Launch this script to test the send_syn function"""
    # 1) SET THE TARGET IP OF YOUR VMs ENVIRONMENT BELOW,
    # 2) launch the script with "python syn_exercise.py"
    # 3) Verify the reception and the response with the synack on the target machine using wireshark
    # 4) Try to set spoof_ip to True and repeat the verification, did the source ip changed?
    target_ip = "192.168.31.1"
    target_port = 8080
    spoof_ip = False


    send_syn(target_ip, target_port, spoof_ip)

