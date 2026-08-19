from helpers import *

import imagecodecs

ENDIANNESS = "<" # Little

class Texture():
    def __init__(self):
        self.Magic = b""
        self.Width = 0
        self.Height = 0
        self.Pitch = 0 # Bytes per row of blocks
        self.MipMapCount = 0
        
        self.TotalHeaderSize = 0
        
        self.TotalFileSize = 0
        
        self.TextureNameOffset = 0
        
        self.TextureName = ""
        
        self.TextureData = b""
        
        self.DecodedTexture = None
        
        
    def ParseTexture(self, f):
        self.Magic = f.read(4) # b"btx\x00"
        
        f.seek(4, 1) # 4 Unknown bytes
        
        self.Width = read_ushort(f, ENDIANNESS)
        self.Height = read_ushort(f, ENDIANNESS)
        self.Pitch = read_ushort(f, ENDIANNESS)
        
        f.seek(2, 1) # 2 Unknown bytes
        
        self.MipMapCount = read_ushort(f, ENDIANNESS)
        
        
        f.seek(6, 1) # 6 Unknown bytes
        
        self.TotalHeaderSize = read_uint(f, ENDIANNESS)
        
        f.seek(4, 1) # Unknown FF 00 00 00
        
        self.TotalFileSize = read_uint(f, ENDIANNESS)
        
        self.TextureNameOffset = read_uint(f, ENDIANNESS)
        
        f.seek(8, 1) # Unknown zeroes
        
        Remaining = self.TotalHeaderSize - 48
        
        self.TextureName = f.read(Remaining).decode("utf-8").rstrip("\x00")
        
        
        self.TextureData = f.read()
        
        
        
    def DecodeBCn(self, num):
        self.DecodedTexture= imagecodecs.bcn_decode(
            self.TextureData,
            num,
            shape=(self.Height, self.Width, 4), 
            
        )
        