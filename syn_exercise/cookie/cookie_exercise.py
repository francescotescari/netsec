import hashlib
import hmac
from time import time

from syn_exercise.cookie.base import *

server_ip = "192.168.1.1"
server_port = 8080
server_mss = 1380
server_sack = True
server_w_scaling = 8
server_window = 60720

mss_values = [536, 1300, 1440, 1460][::-1]

MAX_SYNCOOKIE_AGE = 2


def mss_to_index(mss):
    """Round (lower) the input MSS value to one of the common MSS table and return the relative index and
    the rounded MSS value. Basically encode the MSS value in a 2 bits index."""
    i = 3
    for m in mss_values:
        if mss >= m:
            return i, m
        i -= 1
    return 0, mss_values[0]


def mss_from_index(mss_i):
    """Return MSS value corresponding to the input index in the 4 common MSS table.
    Basically decode the two bits index into the original MSS value"""
    return mss_values[mss_i]


def tcp_time():
    """Return current timestamp in minutes"""
    return round(time() / 60)


def uint32_hash_fields(*args, **kwargs):
    """Hash all the input arguments in a 4 byte integer, with secret key"""
    all_args = [*args] + [*(kwargs.values())]
    data = "|||".join(map(str, all_args))
    hash_bytes = hmac.digest("SECRET_KEY".encode("utf-8"), data.encode("utf-8"), hashlib.sha256)[:4]
    return int.from_bytes(hash_bytes, "big", signed=False)


def encode_sequence_number(ip: str, port: int, minute_timestamp: int, mss_index: int) -> int:
    """Calculate the sequence number hashing ip, port, timestamp and include the mss index and timestamp lowest bits
    Encode the hash in the lowest 24 bits, the highest 8 bits should be TTTTTTMM
    T=timestamp, M=mss_index"""
    # TODO COMPLETE HERE
    # 1) Calculate the hash value of the ip, port and current timestamp
    # 2) Encode 24bits of the hash, the mss_index and timestamp lowest bits in a unique 32bit number
    # 3) Encrypt (xor with the hash of) the sequence number with the source ip and port
    # Q) How hard it is for an attacker to forge a valid cookie, given a source IP and port? Assume MAX_SYNCOOKIE_AGE=2



def decode_sequence_number(sequence_number: int, ip: str, port: int, minute_timestamp: int) -> int:
    """Verify the received sequence number against the received ip port and current timestamp"""
    # TODO COMPLETE HERE
    # 1) Decrypt (xor with the hash of) the cookie with the source ip and port hash
    # 2) Calculate the time difference between the cookie timestamp and the current timestamp
    # 3) Verify that the difference is lower than the MAX_SYNCOOKIE_AGE
    # 4) Calculate the hash value of the ip, port and original timestamp (not the current one)
    # 5) Verify that calculated hash is equal to the hash encoded in the sequence number
    # 6) Decode and return the MSS index


def encode_options(timestamp: int, window_scaling: int, sack: bool, ecn: bool) -> int:
    """Encode the options into the lowest bits of the timestamp.
    The options should be encoded in the lowest 6 bits, as ESWWWW
    E=ecn, S=sack, W=window_scaling"""
    # TODO COMPLETE HERE


def decode_options(timestamp: int) -> (int, int, bool, bool):
    """Decode the options from the lowest bits of the timestamp.
    The options should be decoded from the lowest 6 bits, as ESWWWW
    E=ecn, S=sack, W=window_scaling"""
    # TODO COMPLETE HERE


class SyncookieHandshakeHandler(TcpHandshakeHandler):

    def handle_syn(self, packet: SynPacket) -> SynAckPacket:
        # Choose the socket MSS (decide between the server and the client one)
        mss = min(packet.mss, server_mss)
        # Find the rounded mss and the relative index from the common MSS table (see mss_to_index function)
        mss_index, mss = mss_to_index(mss)

        minute_timestamp = tcp_time()
        # Calculate the sequence number encoding the source ip, port, current timestamp and mss index
        sequence_number = encode_sequence_number(packet.src_ip, packet.src_port, minute_timestamp, mss_index)
        # Calculate the timestamp value encoding the timestamp higher bits, the sack, window scaling and ecn options
        timestamp = round(time())
        timestamp = encode_options(timestamp, packet.w_scaling, packet.sack, packet.ecn)

        # Craft a normal synack packet with the calculate sequence number
        synack = SynAckPacket()
        synack.src_port = server_port
        synack.src_ip = server_ip
        synack.window = server_window
        synack.sequence_number = sequence_number
        synack.ack_number = packet.sequence_number + 1
        synack.sack = packet.sack and server_sack
        synack.w_scaling = server_w_scaling
        synack.mss = mss
        synack.timestamp = timestamp

        return synack

    def handle_ack(self, packet: AckPacket) -> TcpSocket:
        # Get the original sequence_number (ack_number of the client-1)
        original_sequence_number = packet.ack_number - 1
        # Verify the validity of the sequence number against the current minute timestamp, source ip and port
        # Retrieve the MSS value from the common mss table index encoded in the sequence number
        minute_timestamp = tcp_time()
        mss_index = decode_sequence_number(original_sequence_number, packet.src_ip, packet.src_port, minute_timestamp)
        mss = mss_from_index(mss_index)
        # Decode the tcp options encoded in the timestamp echo of the ack value
        timestamp, window_scaling, sack, ecn = decode_options(packet.timestamp_echo)
        # Create the tcp socket with the decoded options
        socket = TcpSocket()
        socket.src_port = packet.src_port
        socket.src_ip = packet.src_ip
        socket.window = packet.window
        socket.sequence_number = packet.ack_number
        socket.ack_number = packet.sequence_number + 1
        socket.mss = mss
        socket.sack = sack
        socket.w_scaling = window_scaling
        socket.ecn = ecn
        return socket


if __name__ == '__main__':
    server = SyncookieHandshakeHandler()
    test_logging_single(server)
    test_forgery_attack(server)
    #test_synflood_attack(server, limit=10000)
