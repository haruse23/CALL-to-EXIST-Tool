from helpers import *
from bitreader import *

from io import BytesIO

ENDIANNESS = "<" # Little

class crilayla():
    def __init__(self):
        self.Magic = b""
        self.UncompressedSize = 0
        self.CompressedSize = 0
        
        self.CompressedData = b""
        self.UncompressedDataHeader = b"" # First 256 bytes of the data are at the end ( uncompressed )
        
        self.OutputDecompressed = BytesIO()
        
    def ReadCrilayla(self, f):
        self.Magic = f.read(8)
        self.UncompressedSize = read_uint(f, ENDIANNESS)
        self.CompressedSize = read_uint(f, ENDIANNESS)
        
        self.CompressedData = f.read(self.CompressedSize)
        self.UncompressedDataHeader = f.read(256)
        
        
    def Levels(self):
        for v in [2, 3, 5, 8]:
            yield v
            
        while True:
            yield 8
            
        
    def DecompressCrilayla(self):
        self.CompressedData = self.CompressedData[::-1]
        
        bitreader = BitReader(self.CompressedData)
        
        minimal_reference_length = 3
        
        while self.OutputDecompressed.tell() < self.UncompressedSize:
            # Read control bit 
            control_bit = bitreader.read_bit()
            
            if control_bit == 0: # Literal
                byte = bitreader.read_bits(8) # Read a byte and store it in the output
                
                self.OutputDecompressed.write( bytes( [byte] ) )
                
            
            elif control_bit == 1:
                # Back-reference
                offset = bitreader.read_bits(13) + minimal_reference_length # Read 13 bits and add 3 (MINIMAL REFERENCE LENGTH) to get offset
                
                reference_length = minimal_reference_length
                
                for lv in self.Levels():
                    value = bitreader.read_bits(lv)
                    reference_length += value
                    
                    if value != (2**lv - 1):  # if the bits of the value are not all 1s
                        break
                

                while reference_length > 0:
                    self.OutputDecompressed.seek(-offset, 1) # Seek back to the beginning of the referenced bytes
                    
                    referenced_byte = self.OutputDecompressed.read(reference_length) # Read the referenced byte
                    
                    self.OutputDecompressed.seek(0, 2) # Go to end of the decompressed output data
                    
                    self.OutputDecompressed.write(referenced_byte) # Add/Write the referenced byte to the output data
                    
                    reference_length -= len(referenced_byte) # Decrease the reference length by the length of the referenced bytes until the While loop ends
                    
                    
                
            
        return self.UncompressedDataHeader + self.OutputDecompressed.getvalue()[::-1]
            
            
            
            
            
            
        
        
        
        
        
    