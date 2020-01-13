#!/bin/python
"""Provides entrypoint and command line interface for starting game server."""
import argparse
from multiplayer import server


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost', dest="host",
                        help='interface the client sends to')
    parser.add_argument('-p', '--port', type=int, default=8080,
                        help='TCP port', dest="port")

    args = parser.parse_args()

    server.run_server(args.host, args.port)
