#!/usr/local/bin/python3.8

import time
import socket
import random
import sys


def usage():
	print(f"Usage: python3.8 {sys.argv[0]} <ip> <seconds of attack>")


def startAttack(victim_ip, duration):
	# TODO: open a socket
	#sock =

	msg = bytes(random.getrandbits(10))
	timeout = time.time() + duration
	sent_packets = 0

	print(f"Attacking {victim_ip} for {duration} seconds")

	while time.time() < timeout:
		victim_port = random.randint(1025, 65356)
		# TODO: send packet

		sent_packets += 1

	print(f"Attack finished. Sent {sent_packets} packets.")


def main():
	if len(sys.argv) != 3:
		usage()
		exit(1)

	startAttack(sys.argv[1], int(sys.argv[2]))


if __name__ == '__main__':
	main()
