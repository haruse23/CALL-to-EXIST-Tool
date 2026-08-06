from helpers import *

ENDIANNESS = "<" # Little

import io

class PAC():
    def __init__(self):
        self.Magic = b""
        self.unk0 = 0 # Version ??
        self.FileNum = 0
        self.FileNum_1 = 0
        
        self.ArchiveName = ""
        
        self.Offsets = []
        
        
        
        
        
    def ReadPACHeader(self, f):
        self.Magic = f.read(4) # b"ARC "
        self.unk0 = read_ushort(f, ENDIANNESS)
        self.FileNum = read_ushort(f, ENDIANNESS)
        self.FileNum_1 = read_uint64(f, ENDIANNESS)
        
        self.ArchiveName = f.read(32).decode("utf-8").rstrip("\x00") # Read 32 bytes, decode them as utf-8, and then strip the null bytes
        
        
        
       
        
    def ReadPACOffsets(self, f):
        for _ in range(self.FileNum):
            self.Offsets.append( read_uint(f, ENDIANNESS) )
            
    
            
            




class PACFileHeader():
    def __init__(self):
        self.ContainedFilesType = ""
        self.FileID = 0
        self.FileUnk = 0 # Hash ??
        self.FilenameLength = 0
        
        self.Filename = ""
        
        
    def ReadFileHeader(self, f):
        self.ContainedFilesType = f.read(4).decode("utf-8").rstrip("\x00") # btls, dyns, mots, dat, facs, prms, etc
        self.ContainedFileID = read_ushort(f, ENDIANNESS) # Will be 0 for all files if they still don't have the last nested files like .tex, .mdl, etc
        
        self.FileID = read_ushort(f, ENDIANNESS)
        self.FileUnk = read_uint(f, ENDIANNESS)
        
        f.seek(2, 1) # Unknown 2 bytes ?
        
        self.FilenameLength = read_ushort(f, ENDIANNESS)
        
        f.seek(4, 1) # Another unknown 4 bytes ?
        
        self.Filename = f.read(self.FilenameLength).decode("utf-8").rstrip("\x00") # Read self.FilenameLength number of bytes, decode them as utf-8, and then strip the null bytes
        
        
        
        
        

        
import os
        

        
def ParsePACArchive(f):
        all_data = f.read()
        
        f.seek(0, 0) # Return to beginning normally
            
            
        pac = PAC()
        
        pac.ReadPACHeader(f)
        
        pac.ReadPACOffsets(f)
        
        align(32, f, f.tell()) # 32-byte alignment
        
        file_header_objs = []

        for p in range(pac.FileNum):
            file_header = PACFileHeader()
            
            file_header.ReadFileHeader(f)
            
            align(32, f, f.tell()) # 32-byte alignment
            
            file_header_objs.append(file_header)
        
        #align(64, f, f.tell()) # 32-byte alignment
        
        File_Dictionaries = []
        
        for offset, file_header_obj in zip(pac.Offsets, file_header_objs): # Create File Dictionary
            f.seek(offset, 0)
            
            FileSize = read_uint(f, ENDIANNESS)
            FileOffsetRelative = read_uint(f, ENDIANNESS)
            
            AbsoluteFileOffset = FileOffsetRelative + offset
            
            f.seek(AbsoluteFileOffset, 0)
            file_data = f.read(FileSize)
            
            File_Dictionaries.append( { "ArchiveName": pac.ArchiveName, "ArchiveSize": len(all_data), "FileName": file_header_obj.Filename, "ContainsFilesOfType": file_header_obj.ContainedFilesType, "FileSize": FileSize, "FileOffset": AbsoluteFileOffset } )
            
            
            
        return File_Dictionaries




def ExtractPACArchive(archive_file_path, output_folder, File_Dictionaries):
    archive_file_name = os.path.basename(archive_file_path)
    
    output_path = f"{output_folder}\\{archive_file_name}_unpacked"
    os.makedirs(output_path, exist_ok=True)
            
    with open(archive_file_path, "rb") as f:
        for file_dict in File_Dictionaries:
            
            file_offset = file_dict["FileOffset"]
            file_size = file_dict["FileSize"]
            file_name = file_dict["FileName"]

            f.seek(file_offset)
            file_data = f.read(file_size)
            print(repr(file_name))       

            
            
            
            path_to_write = f"{output_path}\\{file_name}.{file_dict["ContainsFilesOfType"]}"
            
            print(repr(path_to_write))
            
            with open(path_to_write, "wb") as out:
                out.write(file_data)
            
            
            
            

        