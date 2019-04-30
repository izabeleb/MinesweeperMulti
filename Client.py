"""Defines the Client used to send adn receive data to the server."""
import asyncio
import struct
import json
import MineField

class Client(asyncio.Protocol):
    """Client used to send and receive mine_field data and changes.

    Changes are sent in the following format:
        <packet_length><packet_json>
    The JSON has TWO fields ('HIT' and 'FLAG') with a list of tuples
    specifying the field coordinates where the change occurred. Each packet
    may contain one or both of these fields.

    (eg)
    {
        'HIT': [(0, 0)],
        'FLAG': [(5, 8), (7, 3)]
    }
    """

    def connection_made(self, transport):
        """Establish values pertinent to the server connection.

        Args:
            transport: the TCP connection interface used to send and
                read data to and from the server.
        """
        self.transport = transport
        self.buffer: bytes = b''

    def data_received(self, data: bytes):
        """Handle data read from the server.

        Args:
            data (bytes): the data read from the server socket.
        """
        pass

    def get_server_field(self):
        """Get the mine_filed genenrate by the server."""
        pass

    def send_field_change(self, coords: tuple, change_type: int):
        """Send a local change to the server.

        There are TWO types of changes which can be made:
            1 ) HIT
            2 ) FLAG

        Args:
            coords (tuple): a tuple containing the coordinates of the
                change. (ie. (row, col))
            change_type (in): integer representing the type of change
                made.
        """
        json_packet: bytes = json.dumps({coords: change_type}).encode()
        size_prefix: bytes = Client.get_packet_size(json_packet)
        self.transport.write(size_prefix + json_packet)


def run_client(host: str = 'loclahost', port: int = 8080):
    loop = asyncio.get_event_loop()
    client = Client()
    coro = loop.create_connection(Client, host, port)
    client = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    finally:
        loop.close()
