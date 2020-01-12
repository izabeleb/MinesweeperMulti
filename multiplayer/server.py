"""Defines the server used to connect multiple clients."""
import asyncio
import json
import struct
from typing import Optional
from minesweeper.minefield import MineField


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

        Args:
            row (int): The amount of rows to generate the minefield with.
            col (int): The amount of columns to generate the minefield with.
    """
    transport_list: list = list()
    mine_field: Optional[MineField] = None

    def __init__(self, row: int = 10, col: int = 10):
        self._buffer: bytes = bytes()
        self.transport = None
        self._address: Optional[tuple] = None
        if Server.mine_field is None:
            Server.mine_field = MineField(row, col)

    def connection_made(self, transport):
        """Define values pertinent to the connection ith the client.

        Args:
            transport: the TCP connectioninterface use to send and read
                data to and from the client.
        """
        self.transport = transport
        self._address: tuple = self.transport.get_extra_info('peername')
        self.transport.write(Server.mine_field.encode())
        Server.transport_list.append(self.transport)

        print(f'Accepted connection form {self._address}')

    def data_received(self, data: bytes):
        """Handle data read from the client.

        Data is in JSON format, with any of the following fields:
                   COL  Column number
                   ROW  Row number
                ACTION  The action made by the user (eg. HIT, FLAG, or
                        FIELD)
            MINECHANGE  The location of a mine is being changed. Will
                        contain the sub-fields: 'OLD' and 'NEW'
                        specifying the old and new locations for
                        the mine.
        If the ACTION is FIELD the servers encoded field is returned.

        Args:
            data (bytes): the data read from the client socket.
        """
        self._buffer += data

        while len(self._buffer) > 4:
            packet_length: int = struct.unpack('!I', self._buffer[:4:])[0]

            if len(self._buffer) < 4 + packet_length:
                continue

            self._buffer = self._buffer[4::]

            packet: dict = json.loads(self._buffer[:packet_length:].decode())
            self._buffer = self._buffer[packet_length::]

            affected_row: int = -1
            affected_col: int = -1

            if 'ROW' in packet:
                affected_row = packet['ROW']
            if 'COL' in packet:
                affected_col = packet['COL']
            if 'ACTION' in packet:
                action: str = packet['ACTION']

                if action == "FIELD":
                    packet: bytes = Server.mine_field.encode()
                    self.transport.write(Server.get_packet_size(packet) +
                                         Server.mine_field.encode())
                    print(f'Field sent to '
                          f'{self.transport.get_extra_info("peername")}')
                    continue

                affected_cell = Server.mine_field.get_cell_at(affected_row,
                                                              affected_col)
                if action == 'FLAG':
                    affected_cell.is_flag = True
                    affected_cell.clicked = True
                elif action == 'HIT':
                    affected_cell.clicked = True

            if 'MINECHANGE' in packet:
                self.broadcast_change(packet)
                old_loc: list = packet['MINECHANGE']['OLD']
                new_loc: list = packet['MINECHANGE']['NEW']
                Server.mine_field.get_cell_at(*old_loc).is_mine = False
                Server.mine_field.get_cell_at(*new_loc).is_mine = True

    def broadcast_change(self, change_dict: dict):
        """Broadcast the change made by the user.

        Args:
            change_dict (dict): The dictionary describing the change that was
                made.
        """
        change_json: bytes = json.dumps(change_dict).encode()
        change_length: bytes = Server.get_packet_size(change_json)

        for transport in Server.transport_list:
            if transport != self.transport:
                self.transport.write(change_length + change_json)

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


def run_server(host: str, port: int):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(Server, host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        server.close()
        loop.close()
        print('\n=== Keyboard closed server ===\n')
    finally:
        server.close()
        loop.close()
