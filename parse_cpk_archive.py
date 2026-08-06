from packet import *
from utf import *
from column import *

from io import BytesIO

from crilayla import *

from tqdm.tk import trange
        
        
def ParseDecryptedPacket(f):
    columns_objs = []              
    
    decrypted_packet = ParseEncryptedPacket(f) # cpk, toc, itoc or any packet
    
    dp = BytesIO(decrypted_packet)
    
    utf = UTF()
    
    utf.ReadUTFHeader(dp)
    
    utf.ReadTableHeader(dp)
    
    utf.ReadColumnDefinition(dp)
    
    utf.ReadRows(dp)
    

    for dictionary in utf.UTFColumns:
        flag = dictionary["flag"]
        
        data_storage = utf.GetColumnDataStorage(flag)
        data_type = utf.GetColumnDataType(flag)
        
        name_offset = dictionary["name_offset"]
        
        name = utf.GetColumnName(dp, name_offset)
        
        column = Column()
        
        column.DataStorage = data_storage
        column.DataType = data_type
        column.Name = name
        column.ColumnConstantValue = dictionary["column_constant_value"]
        
        columns_objs.append(column)
        

    
    for k, row_offset in enumerate(utf.UTFRowsOffsets):
        utf.RowsData.append({})
        
        dp.seek(row_offset)
        
        for column in columns_objs:
            if column.DataStorage == DataStorage.STORAGE_NONE:
                utf.RowsData[k][column.Name] = None
                
                continue
                
                
            if column.DataStorage == DataStorage.STORAGE_ZERO:
                utf.RowsData[k][column.Name] = 0
                
                continue
                
                
            if column.DataStorage == DataStorage.STORAGE_CONSTANT:
                utf.RowsData[k][column.Name] = column.ColumnConstantValue
                
                continue
                
                
            if column.DataStorage == DataStorage.STORAGE_PERROW:
                
                
                utf.RowsData[k][column.Name] = utf.ParseRowData(dp, column.DataType)
                
                continue
       
    
    return utf.RowsData
    

import os

import sys

def Parse(f):
    cpk_utf = ParseDecryptedPacket(f) # First packet is cpk packet
    
    cpk_utf_dict = cpk_utf[0]
    
    print(cpk_utf_dict)
    
    cpk_filenum= cpk_utf_dict["Files"]
    
    toc_offset = cpk_utf_dict.get("TocOffset")
    toc_size = cpk_utf_dict.get("TocSize")
    
    Files = []
        
    # Next packet is toc packet if exists
    if toc_offset and toc_size:
        f.seek(toc_offset)
        
        toc_utf = ParseDecryptedPacket(f)
        
        for element in toc_utf:
            print(element)
 
        
        for m in range(cpk_filenum):
            dir_name = toc_utf[m]["DirName"]
            file_name = toc_utf[m]["FileName"]
            
            file_offset = toc_utf[m]["FileOffset"]
            file_size = toc_utf[m]["FileSize"]
            extract_size = toc_utf[m]["ExtractSize"]
            
            f.seek(toc_offset)
            f.seek(file_offset, 1)
            
            file = f.read(file_size)
            
            AbsoluteFileOffset = toc_offset + file_offset
               
            Files.append( {"ArchiveName": "", "DirName": dir_name, "FileName": file_name, "FileOffset":AbsoluteFileOffset, "FileSize":file_size, "ExtractSize":extract_size} )
            
            
            
        
    
    
    htoc_offset = cpk_utf_dict.get("HtocOffset")
    htoc_size = cpk_utf_dict.get("HtocSize")
    
    if htoc_offset and htoc_size:
        f.seek(htoc_offset)
        
        htoc_utf = ParseDecryptedPacket(f)
        
        for element in htoc_utf:
            print(element)
           
           
    etoc_offset = cpk_utf_dict.get("EtocOffset")
    etoc_size = cpk_utf_dict.get("EtocSize")
    
    if etoc_offset and etoc_size:
        f.seek(etoc_offset)
        
        etoc_utf = ParseDecryptedPacket(f)
        
        for element in etoc_utf:
            print(element)
    
    
    
    itoc_offset = cpk_utf_dict.get("ItocOffset")
    itoc_size = cpk_utf_dict.get("ItocSize")
    
    if itoc_offset and itoc_size:
        f.seek(itoc_offset)
        
        itoc_utf = ParseDecryptedPacket(f)
        
        for element in itoc_utf:
            print(element)
    
    
    
    gtoc_offset = cpk_utf_dict.get("GtocOffset")
    gtoc_size = cpk_utf_dict.get("GtocSize")
    
    if gtoc_offset and gtoc_size:
        f.seek(gtoc_offset)
        
        gtoc_utf = ParseDecryptedPacket(f)
        
        for element in gtoc_utf:
            print(element)
            
    
    hgtoc_offset = cpk_utf_dict.get("HgtocOffset")
    hgtoc_size = cpk_utf_dict.get("HgtocSize")
    
    
    if hgtoc_offset and hgtoc_size:
        f.seek(hgtoc_offset)
        
        hgtoc_utf = ParseDecryptedPacket(f)
        
        for element in hgtoc_utf:
            print(element)
            
            
            
            
            
    return Files
    
    
    
def Extract(Files, archive_file_path, output_folder):
    archive_name = os.path.basename(archive_file_path)
    dir_path = f"{output_folder}/{archive_name}_unpacked/{dir_name}"
    os.makedirs(dir_path, exist_ok=True)
            
    with open(archive_file_path, "rb") as f:
        for file in Files:
            dir_name = file["DirName"]
            file_name = file["FileName"]
            
            
            
            extracted_file_path = os.path.join(dir_path, file_name)
            
            file_size = file["FileSize"]
            extract_size = file["ExtractSize"]
            file_offset = file["FileOffset"]
            
            f.seek(file_offset)
            file_data = f.read(file_size)
            
            if file_size != extract_size: # Decompress CRILAYLA if compressed
                compressed_file_object = BytesIO(file_data)
                
                cri_layla = crilayla() # object from the class
                
                cri_layla.ReadCrilayla(compressed_file_object)
                
                file_data = cri_layla.DecompressCrilayla()
            
            
            with open(extracted_file_path, "wb") as out:
                out.write(file_data)


