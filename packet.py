from helpers import *

ENDIANNESS = "<" # Little

class PacketHeader():
    def __init__(self):
        self.Magic = b""
        self.unk0 = 0
        self.PacketSize = 0
        
        
    def ReadPacketHeader(self, f):
        self.Magic = f.read(4)     
        self.PacketMode = read_uint(f, ENDIANNESS)
        self.PacketSize = read_uint64(f, ENDIANNESS)
        
        return self.PacketSize
        



class Packet():
    def __init__(self):
        self.PacketData = b""
        
        self.Magic = b""
        self.TableSize = 0
        
        
        
    def ReadPacketData(self, f, PacketSize):
        self.PacketData = f.read(PacketSize)
        
        
    def DecryptPacketData(self):
        m = 0x0000655F
        t = 0x00004115
        
        out = bytearray(self.PacketData)

        for i in range(len(out)):
            out[i] = out[i] ^ (m & 0xFF)
            m *= t

        return bytes(out)
       
        
        



def ParseEncryptedPacket(f):
    packet_header = PacketHeader()

    packet_size = packet_header.ReadPacketHeader(f)

    packet_data = Packet()

    packet_data.ReadPacketData(f, packet_size)
    
    if packet_header.PacketMode == 0:
        decrypted_packet = packet_data.DecryptPacketData()
        return decrypted_packet
        
    else: # Not always gonna be encrypted
        return packet_data.PacketData
    
    
