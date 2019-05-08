"""Defines the server used to connect multiple clients."""
from minefield import MineField
import asyncio
import struct
import argparse


class Server(asyncio.Protocol):
    """Server used to send and receive mine_field data and changes.

        Changes are sent in the following format:
            <packet_length><packet_json>
        The JSON has TWO fields ('HIT' and 'FLAG') with a list of tuples
        specifying the field coordinates where the change occurred.
        Each packet may contain one or both of these fields.

        (eg)
        {
            'HIT': [(0, 0)],
            'FLAG': [(5, 8), (7, 3)]
        }
    """

    @staticmethod
    def get_packet_size(packet: bytes) -> bytes:
        """Get the encoded packet size in network order.

        Packs the length of the packet into a unsigned short in network
        byte order.

        Args:
            packet (bytes): the encoded packet to be sent to the server.

        Returns:
            (bytes): the encode size of the packet
        """
        return struct.pack('!I', len(packet))

    def __init__(self) -> None:
        self._mine_field = MineField()

    def connection_made(self, transport) -> None:
        """Define values pertinent to the connection ith the client.

        Args:
            transport: the TCP connectioninterface use to send and read
                data to and from the client.
        """
        self.transport = transport
        self._address: tuple = self.transport.get_extra_info('peername')
        self._buffer: bytes = b''
        print(f'Accepted connection form {self.address}')

    def data_received(self, data: bytes) -> None:
        """Handle data read from the client.

        Data is in JSON format, with any of the following fields:
            COL     Column number
            ROW     Row number
            ACTION  The action maade by the user (eg. HIT, FLAG, or
                    FIELD)
        If the ACTION is FIELD the servers encode field is returned.

        Args:
            data (bytes): the data read from the client socket.
        """
        self._buffer += data

        while len(self._buffer) >= 4:
            packet_len: int = struct.unpack('!I', self._buffer[:4:])[0]

    def reply_server_field(self) -> None:
        """Send the server mine_field to the client."""
        pass


def run_server(host: str, port: int):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(Server, host, port)

    server = loop.run_until_complete(coro)
    try:
        loop.run_forecver()
    except KeyboardInterrupt:
        server.close()
        loop.close()
        print('\n=== Keyboard closed server ===\n')
    finally:
        server.close()
        loop.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TCP File Uploader')
    parser.add_argument('--host', default='localhost', dest="host",
                        help='interface the client sends to')
    parser.add_argument('-p', '--port', type=int, default=8080,
                        help='TCP port', dest="port")
    # parser.add_argument('-e', '--encrypt', action='store_true',
    #                   dest='encrypt', help='encrypt the chat communications')

    args = parser.parse_args()

    run_server(args.host, args.port)
