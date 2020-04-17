from time import time

from syn_exercise.cookie.base import *

server_ip = "192.168.1.1"
server_port = 8080
server_mss = 1380
server_sack = True
server_w_scaling = 8
server_window = 60720


class BacklogHandshakeHandler(TcpHandshakeHandler):
    def __init__(self, limit=1000):
        self.backlog = BacklogQueue(limit=limit)

    def handle_syn(self, packet: SynPacket) -> SynAckPacket:
        server_sequence = random_sequence_number()

        # Create a socket structure with the data from the syn and a random sequence number
        socket = TcpSocket()
        socket.src_port = packet.src_port
        socket.src_ip = packet.src_ip
        socket.window = packet.window
        socket.sequence_number = server_sequence
        socket.ack_number = packet.sequence_number + 1
        socket.sack = packet.sack
        socket.w_scaling = packet.w_scaling
        socket.mss = packet.mss

        # Store the half-opened socket in the backlog
        try:
            self.backlog.store(socket.src_ip, socket.src_port, socket)
        except BacklogException as e:
            raise SynFailed("Failed to store half-open connection in the backlog") from e

        # Return syn ack response
        synack = SynAckPacket()
        synack.src_port = server_port
        synack.src_ip = server_ip
        synack.window = server_window
        synack.sequence_number = server_sequence
        synack.ack_number = packet.sequence_number + 1
        synack.sack = packet.sack and server_sack
        synack.w_scaling = server_w_scaling
        synack.mss = server_mss
        synack.timestamp = round(time())
        return synack

    def handle_ack(self, packet: AckPacket) -> TcpSocket:
        # Retrieve the stored socket
        try:
            socket = self.backlog.get(packet.src_ip, packet.src_port)
        except KeyError:
            raise InvalidAck("No handshake going on with this ip/port")
        self.backlog.delete(packet.src_ip, packet.src_port)
        # Now verify the sequence number
        if packet.ack_number != socket.sequence_number + 1:
            raise InvalidAck("Wrong ack number")
        if packet.sequence_number != socket.ack_number:
            raise InvalidAck("Wrong sequence number")

        socket.open = True
        return socket


if __name__ == '__main__':
    server = BacklogHandshakeHandler()
    test_logging_single(server)
    test_forgery_attack(server)
    test_synflood_attack(server, limit=1001)