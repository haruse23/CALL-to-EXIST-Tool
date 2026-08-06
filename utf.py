from helpers import *




# ENUMS
from enum import IntEnum

class DataStorage(IntEnum):
    STORAGE_MASK = 0xF0
    
    STORAGE_NONE = 0x00,
    STORAGE_ZERO = 0x10,
    STORAGE_CONSTANT = 0x30,
    STORAGE_PERROW = 0x50,




class DataType(IntEnum):
    DATATYPE_MASK = 0x0F
    
    UINT8 = 0
    UINT8_1 = 1
    UINT16 = 2
    UINT16_1 = 3
    UINT32 = 4
    UINT32_1 = 5
    UINT64 = 6
    UINT64_1 = 7
    FLOAT = 8
    STRING = 0xA
    BYTEARRAY = 0xB
        
        
ENDIANNESS = ">" # Big

class UTF(): # @UTF Chunk
    def __init__(self):
        # UTF Header
        self.Magic = b"" # @UTF
        self.TableSize = 0
        
        # Table Header
        self.RowsOffset = 0
        self.StringsOffset = 0
        self.DataOffset = 0
        self.TableName = 0
        self.ColumnsNumber = 0 # Unsigned Short (2 Bytes)
        self.RowLength = 0 # in Bytes - Unsigned Short (2 Bytes)
        self.RowsNumber = 0
        
        
        self.UTFColumns = []
        
        self.UTFRowsOffsets = []
        
        self.RowsData= []
        


    
    def ReadUTFHeader(self, f):
        self.Magic = f.read(4)
        self.TableSize = read_uint(f, ENDIANNESS)
        
        print(self.Magic)
        print(self.TableSize)
    
    def ReadTableHeader(self, f):
        self.RowsOffset = read_uint(f, ENDIANNESS)
        self.StringsOffset = read_uint(f, ENDIANNESS)
        self.DataOffset = read_uint(f, ENDIANNESS)
        
        # Table starts after UTF Header (8 Bytes), add 8 to make an absolute offset
        self.TableSize += 8
        self.RowsOffset += 8
        self.StringsOffset += 8
        self.DataOffset += 8
        
        self.TableName = read_uint(f, ENDIANNESS)
        
        self.ColumnsNumber = read_ushort(f, ENDIANNESS)
        self.RowLength = read_ushort(f, ENDIANNESS)
        
        self.RowsNumber = read_uint(f, ENDIANNESS)
        
        print("Columns:", self.ColumnsNumber)
        print("RowLength:", self.RowLength)
        print("Rows:", self.RowsNumber)
        print("Position:", hex(f.tell()))
        
    def ReadColumnDefinition(self, f):
        for i in range(self.ColumnsNumber):
            ColumnFlag = f.read(1)[0] # int instead of byte
            
            if ColumnFlag == 0:
                f.seek(3, 1)
                ColumnFlag = f.read(1)[0]
                
            ColumnNameOffset = read_uint(f, ENDIANNESS) # Offset into the Strings Table
            
            ColumnValue = None # In case the if-condition is not satisified, the variable needs a value to exist
          
            if ColumnFlag & DataStorage.STORAGE_MASK == DataStorage.STORAGE_CONSTANT:
                ColumnValue = self.ParseRowData(f, ColumnFlag & DataType.DATATYPE_MASK) # Store the constant value of the column, if it exists
            
            self.UTFColumns.append( {"index": i, "flag": ColumnFlag, "name_offset": ColumnNameOffset, "column_constant_value": ColumnValue} )
            
            
            
            
    def ReadRows(self, f):
        for j in range(self.RowsNumber):
            self.UTFRowsOffsets.append( f.tell() )
            
            f.seek(self.RowLength, 1)
            
            
    def ParseRowData(self, row_data_file_object, data_type):
        if data_type == DataType.UINT8 or data_type == DataType.UINT8_1:
            return read_uint8(row_data_file_object, ENDIANNESS)
        
        if data_type == DataType.UINT16 or data_type == DataType.UINT16_1:
            return read_ushort(row_data_file_object, ENDIANNESS)
        
        if data_type == DataType.UINT32 or data_type == DataType.UINT32_1:
            return read_uint(row_data_file_object, ENDIANNESS)
        
        if data_type == DataType.UINT64 or data_type == DataType.UINT64_1:
            return read_uint64(row_data_file_object, ENDIANNESS)
        
        if data_type == DataType.FLOAT:
            return read_float(row_data_file_object, ENDIANNESS)
        
        if data_type == DataType.STRING:
            offset_into_strings_section = read_uint(row_data_file_object, ENDIANNESS)
            
            current_position = row_data_file_object.tell() # Save position
            
            row_data_file_object.seek(self.StringsOffset + offset_into_strings_section)
 
            string = read_cstring(row_data_file_object)
            
            row_data_file_object.seek(current_position, 0) # Restore position
            
            return string
            
        
        if data_type == DataType.BYTEARRAY:
            offset_into_data_section = read_uint(row_data_file_object, ENDIANNESS)
            
            size = read_uint(row_data_file_object, ENDIANNESS)
            
            current_position = row_data_file_object.tell() # Save position
            
            row_data_file_object.seek(self.DataOffset + offset_into_data_section)
            
            databytes =  row_data_file_object.read(size)
            
            row_data_file_object.seek(current_position, 0) # Restore position
            
            return databytes
        
        
    
    
    def GetColumnDataStorage(self, flag):
        return flag & DataStorage.STORAGE_MASK
        
        
    def GetColumnDataType(self, flag):
        return flag & DataType.DATATYPE_MASK
        
    def GetColumnName(self, f, name_offset):
        f.seek( self.StringsOffset + name_offset )
        
        return read_cstring(f)
        
    
    
            
            
            
            

        
        
        
        
        
        