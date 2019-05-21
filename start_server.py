#!/bin/python
from multiplayer import Server
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TCP File Uploader')
    parser.add_argument('--host', default='localhost', dest="host",
                        help='interface the client sends to')
    parser.add_argument('-p', '--port', type=int, default=8080,
                        help='TCP port', dest="port")
    # parser.add_argument('-e', '--encrypt', action='store_true',
    #                   dest='encrypt', help='encrypt the chat communications')

    args = parser.parse_args()

    Server.run_server(args.host, args.port)
