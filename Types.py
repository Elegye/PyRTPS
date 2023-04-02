from enum import Enum
import ctypes
from math import pow

class Endianness(Enum):
    LITTLE_ENDIAN   = True #(1)
    BIG_ENDIAN      = False #(0)

"""VendorIDs as defined by DDS Foundation.

https://www.dds-foundation.org/dds-rtps-vendor-and-product-ids/

"""
class VendorId(Enum):
    RTI_CONNEXT_DDS = (0x01, 0x01)
    OPEN_SPLICE_DDS = (0x01, 0x02)
    OPEN_DDS        = (0x01, 0x03)
    MIL_DDS         = (0x01, 0x04)
    INTERCOM_DDS    = (0x01, 0x05)


"""Submessage Kind

"""
class SubMessage(Enum):
    PAD             = 0x01
    INFO_TS         = 0x09
    INFO_DST        = 0x0e
    INFO_SRC        = 0X0c
    HEARTBEAT       = 0x07
    HEARTBEAT_FRAG  = 0x13
    ACKNACK         = 0x06
    NACK_FRAG       = 0x12
    DATA            = 0x15


"""SequenceNumber defines a 64-bit signed integer, that can take values in the range -2^63 <= N <= 2^63 - 1
See RTPS section 8.3.5.4.

SequenceNumber should usually start at 1.
"""
class SequenceNumber:

    def __init__(self, high: int, low: int) -> None:
        self.high = ctypes.c_ulong(high)
        self.low = ctypes.c_ulong(low)

    def value(self) -> int:
        return int(self.high.value * pow(2, 32) + self.low.value)