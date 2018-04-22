#!/usr/bin/env python3
import asyncio
import socket

BIND_ADDR = "0"
BROADCAST_ADDR ="10.128.255.255" 
PORT = 1337


class _ChatProtocol(asyncio.Protocol):
    """A protocol for chatting among peers.
    """
    transport = None

    @classmethod
    def connection_made(cls, transport):
        sock = transport.get_extra_info("socket")
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        cls.transport = transport

    def datagram_received(self, data, addr):
        ip, port = addr
        message = data.decode()
        print("\n{} said {}".format(ip, message))


def say(message):
    _ChatProtocol.transport.sendto(message.encode(), (BROADCAST_ADDR, PORT))


async def main():
    while True:
        line = await loop.run_in_executor(None, input, "? ")
        cmd, *args = line.split(" ")
        if cmd.lower() == "say":
            message = " ".join(args)
            print("Say: " + message)
            say(message)
        else:
            print("Unknown command: {}".format(cmd))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    protocol = loop.create_datagram_endpoint(
        _ChatProtocol,
        local_addr=(BIND_ADDR, PORT)
    )
    tasks = (protocol, main())
    loop.run_until_complete(asyncio.gather(*tasks))
