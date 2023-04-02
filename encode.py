import time
import socket
import struct
from Types import *
import SubMessages
from typing import Tuple

def make_ip(proto, source_ip, dest_ip, ident=3597):
    source_address = socket.inet_aton(source_ip)
    dest_address = socket.inet_aton(dest_ip)
    header_length = 5
    return struct.pack(
        '!BBBHHHBBH4s4s',
        4, # Version: 4 bits                          B
        header_length, # IHL: Internet Header Length (4 bits)   B
        0, # Type of Service (8 bits)                           B
        64, # Total Length (in octets) (16 bits)                H
        ident, # Identification (16 bits)                       H
        0, # Fragment offset (13bits) + Flags (3bits) = 16 bits H
        255, # Time To Live (8bits)                             B
        proto, # Protocol (8 bits)                              B
        0, # Header Checksum (16bits)                           H
        source_address, # Source Address (32 bits)              4s
        dest_address # Dest Address (32 bits)                   4s
    )

"""Make a TCP Header. See RFC793 (3.1. Header Format)
:param source_port: 

"""
def make_tcp(source_port: int, dest_port: int, payload, seq=123, ackseq=0,
    fin=False, syn=True, rst=False, psh=False, ack=False, urg=False,
    window=5840):
    offset_res = (5 << 4) | 0
    flags = (fin | (syn << 1) | (rst << 2) | 
             (psh <<3) | (ack << 4) | (urg << 5))
    return struct.pack(
        '!HHLLBBHHH',
        source_port,
        dest_port,
        seq,
        ackseq,
        offset_res, 
        flags,
        window,
        0,
        0)

def make_udp(source_port, dest_port, payload, checksum=0):
    # Source port and Dest Port are 16 bits length => (unsigned short)
    return struct.pack(
        "!HHL",
        source_port,
        dest_port,
        8 + len(payload))

def make_rtps(
        submessage: SubMessages,
        vendor: VendorId = VendorId.RTI_CONNEXT_DDS,
        version: tuple[int, int] = (2,1),
        endianness: Endianness = Endianness.BIG_ENDIAN
    ):
    rtps_packet = struct.pack("!4sbbBBIIbI",
        "RTPS".encode("utf-8"),
        version[0], version[1],                         # Major Minor
        vendor.value[0], vendor.value[1],               # VendorID
        0x00000000,                                     # GUIDPrefix: HostID
        0x00010901,                                     # GUIDPrefix: AppID
        endianness.value,                               # Endianness
        submessage.type().value,                        # SubMessageID
    )
    submessage_packet = submessage.construct(endianness)
    print(rtps_packet)
    print(submessage_packet)
    rtps_packet += submessage_packet
    return rtps_packet



msgClient = "Hello Server"
payload = str.encode(msgClient)

HOST = socket.gethostbyname(socket.gethostname())
addrPort = ("", 9999)

# Créer un socket UDP coté client
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

rtps = make_rtps(SubMessages.Heartbeat())
print(rtps)

print(socket.IPPROTO_UDP)

s.sendto(rtps, addrPort)