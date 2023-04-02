from abc import ABC, abstractmethod, abstractproperty
import struct

import Types

class SubMessage(ABC):

    @abstractproperty
    def type() -> Types.SubMessage:
        pass

    @abstractmethod
    def construct(self) -> bytes:
        pass

class Heartbeat(SubMessage):

    def type(self) -> Types.SubMessage:
        return Types.SubMessage.HEARTBEAT

    def construct(self,
        endianness: Types.Endianness,
        final: bool = True,
        liveliness: bool = True
    ) -> bytes:
        flags = (endianness.value | (final << 1) | (liveliness << 2))
        elements = struct.pack(
            "IIHHB",
            0x000100c2, # readerId
            0x000100c7, # writerId
            Types.SequenceNumber(0, 1).value(),    # First sequence number
            Types.SequenceNumber(0, 2).value(),     # Second sequence number
            1       # Count
        )
        print(29)
        header = struct.pack("bH", flags, 0) # 0 because last submessage.
        print("Header: ", header)
        header += elements
        print("Full: ", header)
        return header
    
class Data(SubMessage):

    def type(self) -> Types.SubMessage:
        return Types.SubMessage.DATA
    
    def construct(self) -> bytes:
        return struct.pack(
            "!",
            
        )