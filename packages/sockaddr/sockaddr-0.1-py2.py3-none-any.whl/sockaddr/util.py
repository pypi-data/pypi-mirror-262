import binascii
import socket

from typing import Union

from .addr import *

af_mapping: dict[int, sockaddr_storage] = {
    0: sockaddr_storage,
    socket.AF_UNIX: sockaddr_un,
    socket.AF_INET: sockaddr_in,
    socket.AF_INET6: sockaddr_in6,
    socket.AF_NETLINK: sockaddr_nl,
    socket.AF_X25: sockaddr_x25,
    socket.AF_APPLETALK: sockaddr_atalk,
    socket.AF_PACKET: sockaddr_ll,
}


def from_bytes(b: bytes, pad_with_zero: bool = True) -> ctypes.Structure:
    """Returns a matching sockaddr_ for the bytes.

    May raise ValueError on invalid lengths"""
    if b[0] not in af_mapping.keys():
        raise ValueError(f"Undefined sa_family_t type: {b[0]}")
    sa_family = af_mapping[b[0]]

    if pad_with_zero:
        b = b + (b"\x00" * (ctypes.sizeof(sa_family) - len(b)))

    return sa_family.from_buffer_copy(b)


def from_hex(h: str, pad_with_zero: bool = True) -> ctypes.Structure:
    """Returns a matching sockaddr_ for the hex string.

    May raise a ValueError on invalid lengths"""
    return from_bytes(binascii.unhexlify(h), pad_with_zero)


def inet_addr(sockaddr: Union[sockaddr_in, sockaddr_in6]) -> str:
    if type(sockaddr) is sockaddr_in:
        return socket.inet_ntop(socket.AF_INET, sockaddr.sin_addr)
    elif type(sockaddr) is sockaddr_in6:
        return socket.inet_ntop(socket.AF_INET6, sockaddr.sin6_addr)

    raise TypeError("Invalid type")


def inet_port(sockaddr: Union[sockaddr_in, sockaddr_in6]) -> int:
    if type(sockaddr) is sockaddr_in:
        return sockaddr.sin_port
    elif type(sockaddr) is sockaddr_in6:
        return sockaddr.sin6_port

    raise TypeError("Invalid type")
