import sys
from abc import ABC, abstractmethod
from random import randint


class TcpPacket:
    # There are many field, but we put only the ones interesting for the exercise
    src_port = None
    src_ip = None
    window = 65535
    sequence_number = None
    ack_number = None
    flags = ""

    def __str__(self):
        return "FROM %s:%d, W=%d, SEQ=%d, ACK=%d, F=%s" % (
            self.src_ip, self.src_port, self.window, self.sequence_number, self.ack_number, self.flags)

    def __repr__(self):
        return self.__class__.__name__ + " [" + str(self) + "]"


class SynPacket(TcpPacket):
    flags = "S"
    sack = True
    w_scaling = 8
    mss = 1500
    ecn = True

    def __str__(self):
        return "%s, WS=%r, MSS=%r, SACK=%r, ECN=%r" % (super().__str__(), self.w_scaling, self.mss, self.sack, self.ecn)


class SynAckPacket(SynPacket):
    timestamp = None
    flags = "SA"

    def __str__(self):
        return "%s, TS=%r" % (super().__str__(), self.timestamp)


class AckPacket(TcpPacket):
    timestamp_echo = None
    flags = "A"

    def __str__(self):
        return "%s, TSE=%r" % (super().__str__(), self.timestamp_echo)


class BacklogException(Exception):
    pass


class BacklogQueue:

    @staticmethod
    def _key(ip, port):
        return str(ip) + "_" + str(port)

    def __init__(self, limit):
        self._store = {}
        self._limit = limit

    def store(self, ip, port, socket):
        if len(self._store) >= self._limit:
            raise BacklogException("Backlog queue is full")
        self._store[self._key(ip, port)] = socket

    def get(self, ip, port):
        return self._store[self._key(ip, port)]

    def delete(self, ip, port):
        del self._store[self._key(ip, port)]


class TcpSocket:
    src_port = None
    src_ip = None
    window = 65535
    sequence_number = None
    ack_number = None
    flags = ""
    mss = 1500
    sack = False
    w_scaling = 8
    open = False
    ecn = True


class TcpHandshakeHandler(ABC):

    @abstractmethod
    def handle_syn(self, packet: SynPacket) -> SynAckPacket:
        raise NotImplementedError

    @abstractmethod
    def handle_ack(self, packet: AckPacket) -> TcpSocket:
        raise NotImplementedError


class InvalidAck(Exception):

    def __init__(self, reason: str):
        super().__init__(reason)


class SynFailed(Exception):
    pass


class AckFailed(Exception):
    pass


class ClientSocket:

    def do_handshake(self, server: TcpHandshakeHandler):
        syn = self._do_syn()
        synack = server.handle_syn(syn)
        ack = self._do_ack(synack)
        server_socket = server.handle_ack(ack)
        return server_socket

    def _do_syn(self) -> SynPacket:
        raise NotImplementedError

    def _do_ack(self, synack: SynAckPacket):
        raise NotImplementedError


def random_sequence_number():
    return randint(0, 0xffffffff)


class ClientSocketImpl(ClientSocket):
    src_port = None
    src_ip = None
    window = 64240
    sequence_number = None
    ack_number = 0
    sack = True
    w_scaling = 8
    mss = 1500

    def __init__(self):
        self.src_ip = random_ip()
        self.src_port = random_private_port()

    def _do_syn(self) -> SynPacket:
        self.sequence_number = random_sequence_number()

        syn = SynPacket()
        syn.src_port = self.src_port
        syn.src_ip = self.src_ip
        syn.window = self.window
        syn.sequence_number = self.sequence_number
        syn.ack_number = self.ack_number
        syn.sack = self.sack
        syn.w_scaling = self.w_scaling
        syn.mss = self.mss
        return syn

    def _do_ack(self, synack: SynAckPacket):
        # Check the sequence number
        if synack.ack_number != self.sequence_number + 1:
            raise SynFailed("Invalid synack seq from server")
        self.sequence_number = synack.ack_number
        self.ack_number = synack.sequence_number + 1

        ack = AckPacket()
        ack.src_port = self.src_port
        ack.src_ip = self.src_ip
        ack.window = self.window
        ack.sequence_number = self.sequence_number
        ack.ack_number = self.ack_number
        ack.timestamp_echo = synack.timestamp
        return ack


class LoggingClientSocket(ClientSocketImpl):

    def _do_syn(self) -> SynPacket:
        pkt = super()._do_syn()
        print("C-->S %r" % pkt)
        return pkt

    def _do_ack(self, synack: SynAckPacket):
        print("C<--S %r" % synack)
        pkt = super()._do_ack(synack)
        print("C-->S %r" % pkt)
        return pkt


def test_logging_single(server):
    client_socket = LoggingClientSocket()
    try:
        server_socket = client_socket.do_handshake(server)
    except SynFailed as e:
        print("Handshake failed during syn handling", e)
    except AckFailed as e:
        print("Handshake failed during ack handling", e)
    except Exception as e:
        print("Handshake failed unexpectedly", e)
    else:
        print("Handshake successful, opened socket: %s:%d" % (server_socket.src_ip, server_socket.src_port))


class ClientForgeryAcknum(ClientSocketImpl):

    def _do_ack(self, synack: SynAckPacket):
        ack = super()._do_ack(synack)
        ack.ack_number += 1
        return ack


def random_ip():
    """Return a random ip address."""
    return ".".join(map(str, (randint(1, 255) for _ in range(4))))


def random_private_port():
    """Return a random port number among the private ports."""
    return randint(49152, 65535)


def random_client_socket(clazz):
    client = clazz()
    client.src_ip = random_ip()
    client.src_port = random_private_port()
    return client


def _test_handshake(client, server, expected_exception=None):
    try:
        client.do_handshake(server)
    except Exception as e:
        if expected_exception is None or not isinstance(e, expected_exception):
            return e
        return True
    if expected_exception is not None:
        return False
    return True


def test_forgery_attack(server):
    failed = [0]

    def test(condition, fail_msg):
        failed[0] += 1
        if isinstance(condition, Exception):
            failed.append("Exception: " + str(condition) + " while testing if " + fail_msg)
            raise condition
        elif not condition:
            failed.append(fail_msg)

    client = random_client_socket(ClientForgeryAcknum)
    test(_test_handshake(client, server, InvalidAck), "Server allowed ack with wrong ack number")
    client = random_client_socket(ClientSocketImpl)
    test(_test_handshake(client, server, None), "The handshake failed for a valid client")


    print("[%d/%d] forgery tests passed" % (failed[0] - len(failed) + 1, failed[0]))
    for i in range(1, len(failed)):
        print(" - Fail %d: %s" % (i, failed[i]))


class SynFlooderClient(ClientSocketImpl):

    def do_handshake(self, server: TcpHandshakeHandler):
        try:
            server.handle_syn(self._do_syn())
        except Exception as e:
            raise SynFailed("Server didn't handled the syn packet", e)


def test_synflood_attack(server, limit):
    client = SynFlooderClient()
    handled = 0
    dropped = 0
    for i in range(limit):
        client.src_ip = random_ip()
        client.src_port = random_private_port()
        try:
            client.do_handshake(server)
            handled += 1
        except SynFailed:
            dropped += 1
    print("[%s] Server handled %d/%d syn packets" % (("PASS" if dropped == 0 else "FAIL"), handled, handled + dropped))
