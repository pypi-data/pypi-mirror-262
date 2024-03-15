import ctypes

# Without this, the comments at the end of each field will break
# fmt:off

class sockaddr_un(ctypes.Structure):
    """UNIX Socket

    man 7 unix
    Defined in <linux/un.h>"""

    _fields_ = [
        ("sun_family", ctypes.c_ushort),    # AF_UNIX (POSIX: AF_LOCAL)
        ("sun_path", ctypes.c_char * 108),  # Pathname
    ]


class sockaddr_in(ctypes.Structure):
    """IPv4 Socket

    man 7 ip
    sys/socket.h
    <linux/in.h>
    <netinet/in.h>"""

    _fields_ = [
        ("sin_family", ctypes.c_ushort),    # AF_INET
        ("sin_port", ctypes.c_ushort),      # port number
        ("sin_addr", ctypes.c_byte * 4),    # IPv4 address
        ("__pad", ctypes.c_byte * (8)),     # Padding to 16 bytes
    ]


class sockaddr_in6(ctypes.Structure):
    """IPv6 Socket

    man 7 ipv6
    <netinet/in.h>"""

    _fields_ = [
        ("sin6_family", ctypes.c_ushort),   # AF_INET6
        ("sin6_port", ctypes.c_ushort),     # port number
        ("sin6_flowinfo", ctypes.c_uint32), # IPv6 flow identifier
        ("sin6_addr", ctypes.c_byte * 16),  # IPv6 address
        ("sin6_scope_id", ctypes.c_uint32), # Scope ID
    ]


class sockaddr_nl(ctypes.Structure):
    """Netlink Socket

    man 7 netlink
    <linux/netlink.h>"""

    _fields_ = [
        ("nl_family", ctypes.c_ushort),     # AF_NETLINK
        ("nl_pad", ctypes.c_ushort),        # Zero
        ("nl_pid", ctypes.c_uint32),        # Netlink socket (usually the pid, but check the man page!)
        ("nl_groups", ctypes.c_uint32),     # Bitmask with every bit representing a netlink group number.
    ]


class sockaddr_x25(ctypes.Structure):
    """ITU-T X.25 Socket

    man 7 x25
    <linux/x25.h>"""

    _fields_ = [
        ("sx25_family", ctypes.c_ushort),   # AF_X25
        ("sx25_addr", ctypes.c_char * 16),  # Char array that forms the X.121 address
    ]


class sockaddr_atalk(ctypes.Structure):
    """AppleTalk Socket
    
    man 7 ddp
    <netatalk/at.h>"""
    _fields_ = [
        ("sat_family", ctypes.c_ushort),    # AF_APPLETALK
        ("sat_port", ctypes.c_ubyte),       # port number (<127 are reserved)
        ("sat_s_net", ctypes.c_ushort),     # Host network
        ("sat_s_node", ctypes.c_ubyte),     # Host node number
    ]

class sockaddr_ll(ctypes.Structure):
    """Packet interface on device level
    
    man 7 packet
    <net/ethernet.h>
    <linux/if_packet.h>"""
    _fields_ = [
        ("sll_family", ctypes.c_ushort),    # AF_PACKET
        ("sll_protocol", ctypes.c_ushort),  # Physical layer protocol
        ("sll_ifindex", ctypes.c_int),      # Interface number (man 7 netdevice) (0 = any)
        ("sll_hatype", ctypes.c_ushort),    # ARP hardware type
        ("sll_pkttype", ctypes.c_ubyte),    # Packet type (PACKET_HOST, PACKET_BROADCAST, etc.)
        ("sll_halen", ctypes.c_ubyte),      # Length of address
        ("sll_addr", ctypes.c_char * 8),    # Physical layer address
    ]


class sockaddr_storage(ctypes.Structure):

    _fields_ = [
        ("ss_family", ctypes.c_ushort),     # address family
        ("__data", ctypes.c_ubyte * 124)    # data
    ]
