import customtkinter as ctk
from tkinter import filedialog, ttk, Menu

import parse_cpk_archive

import pac

import threading

from PIL import Image

import os

from io import BytesIO

import crilayla

import texture

Dictionary = {"file_path": "", "folder_path": "", "FilesToExtract": [], "extension": "", "ArchiveName": "", "ArchiveSize": 0}

from pathlib import Path

def resource_path(relative_path):
    return str(Path(__file__).resolve().parent / relative_path)
    
# Wrapper around parser
def parse_cpk(source):
    if isinstance(source, str):
        # Source is a file path
        with open(source, "rb") as f:
            files = parse_cpk_archive.Parse(f)
            archive_name = os.path.basename(source)
            data_size = os.path.getsize(source)
            
            Dictionary["FilesToExtract"] = files
            Dictionary["ArchiveName"] = archive_name
            Dictionary["ArchiveSize"] = data_size
            Dictionary["ArchivePath"] = source
            
    else:
        # Source is a BytesIO object
        files = parse_cpk_archive.Parse(source)
        archive_name = None
        data_size = len(source.getvalue())
        
        Dictionary["FilesToExtract"] = files
        Dictionary["ArchiveName"] = archive_name
        Dictionary["ArchiveSize"] = data_size
    
        
    Dictionary["extension"] = ".cpk"
    
    app.after(0, lambda: update_tree())
    
    app.after(0, lambda: update_archive_name_label(archive_name))
    app.after(0, lambda: update_archive_size_label(data_size))
    app.after(0, update_archive_filecount_label)
    app.after(0, update_showing_label)


def parse_pac(source):
    if isinstance(source, str):
        # Source is a file path
        with open(source, "rb") as f:
            files = pac.ParsePACArchive(f)
            archive_name = files[0]["ArchiveName"] 
            data_size = os.path.getsize(source)
            
            Dictionary["FilesToExtract"] = files
            Dictionary["ArchiveName"] = archive_name
            Dictionary["ArchiveSize"] = data_size
            Dictionary["ArchivePath"] = source
            
    else:
        # Source is a BytesIO object
        files = pac.ParsePACArchive(source)
        archive_name = files[0]["ArchiveName"]
        data_size = files[0]["ArchiveSize"]
        
        Dictionary["FilesToExtract"] = files
        Dictionary["ArchiveName"] = archive_name
        Dictionary["ArchiveSize"] = data_size
        Dictionary["ArchivePath"] = source
    
    
    Dictionary["extension"] = ".pac"
    
    app.after(0, lambda: update_tree())
    
    app.after(0, lambda: update_archive_name_label(archive_name))
    app.after(0, lambda: update_archive_size_label(data_size))
    app.after(0, update_archive_filecount_label)
    app.after(0, update_showing_label)

# Size formatting
def format_size(size):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

tree_history = []

# Save tree history
def save_history():
    current_items = []

    for item in tree.get_children():
        current_items.append(tree.item(item)["values"])

    tree_history.append({
        "tree": current_items,
        "extension": Dictionary["extension"],
        "FilesToExtract": Dictionary["FilesToExtract"],

        "archive_name": Dictionary["ArchiveName"],
        "archive_size": Dictionary["ArchiveSize"],
        "archive_filecount": len( Dictionary["FilesToExtract"] ),
        "showing": showing_label.cget("text")
    })
    
    
# Populate/update the treeview
def update_tree():
    tree.delete(*tree.get_children())
    
    ext = Dictionary["extension"]
    
    if ext == ".cpk":
        for file in Dictionary["FilesToExtract"]:
            tree.insert(
                "",
                "end",
                values=(
                    file["DirName"],
                    file["FileName"],
                    file["FileSize"],
                    file["ExtractSize"],
                    file["FileOffset"],
                    ""
                )
            )
        
    else:
        for file_dict in Dictionary["FilesToExtract"]:
            tree.insert(
                "",
                "end",
                values=(
                    "",
                    file_dict["FileName"],
                    file_dict["FileSize"],
                    "",
                    file_dict["FileOffset"],
                    file_dict["ContainsFilesOfType"]
                    
                )
            )
            
            

    
    
        
      
    
    
# Background thread to stop UI from freezing    
def run_in_background(func, *args, **kwargs):
    thread = threading.Thread(
        target=func,
        args=args,
        kwargs=kwargs,
        daemon=True
    )
    thread.start()


def update_archive_name_label(archive_name):
    # Updating archive name label
    archive_name_label.configure(
        text=f"Archive Name: {archive_name}"
    )
    
def update_archive_size_label(data_size):
    archive_size = format_size( data_size )
        
    # Updating archive size label
    archive_size_label.configure(
        text=f"Archive Size: {archive_size}"
    )
    
def update_archive_filecount_label():
    # Updating archive filecount label
    archive_filecount_label.configure(
        text=f"Archive FileCount: {len(Dictionary["FilesToExtract"])}"
    )
    
def update_showing_label():
    visible_files = len(tree.get_children())
    all_files = len(Dictionary["FilesToExtract"])
    
    showing_label.configure(text=f"Showing {visible_files} out of {all_files} files")
    
def open_file():
    file_path = filedialog.askopenfilename()

    if not file_path:
        return

    Dictionary["file_path"] = file_path


    Dictionary["extension"] = os.path.splitext(file_path)[1].lower()
    
    
    
    if Dictionary["extension"] == ".cpk":
        save_history()
        run_in_background(parse_cpk, file_path)
    else:
        save_history()
        run_in_background(parse_pac, file_path)
        
    
    
    
        
def open_folder():
    folder_path = filedialog.askdirectory()
    
    if not folder_path:
        return
        
    Dictionary["folder_path"] = folder_path
    
    """if folder_path:
        folder_box.delete(0, "end")
        folder_box.insert(0, folder_path)"""
    

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Create the main window
app = ctk.CTk()
app.title("Tokyo Ghoul: re [CALL to EXIST] Tool 1.0.0")
app.geometry("1600x977")
app.resizable(width=True, height=True)  # Allow resizing
app.iconbitmap(resource_path("icons/app.ico"))



# Archive name label
archive_name_label = ctk.CTkLabel(app, font=("Helvetica", 20), text_color="grey", text="Archive Name: ")

archive_name_label.place(
    relx=0.45,
    rely=0.001,
    relwidth=0.2,
    relheight=0.05
)

# Archive size label
archive_size_label = ctk.CTkLabel(app, font=("Helvetica", 20), text_color="grey", text="Archive Size: ")

archive_size_label.place(
    relx=0.65,
    rely=0.001,
    relwidth=0.15,
    relheight=0.05
)

# Archive filecount label
archive_filecount_label = ctk.CTkLabel(app, font=("Helvetica", 20), text_color="grey", text="Archive FileCount: ")

archive_filecount_label.place(
    relx=0.85,
    rely=0.001,
    relwidth=0.15,
    relheight=0.05
)


# Icons
Icons = {
    "open_file": ctk.CTkImage(Image.open(resource_path("icons/open_file.png")), size=(40,40)),
    "open_folder": ctk.CTkImage(Image.open(resource_path("icons/open_folder.png")), size=(40,40)),
    "extract_cpk": ctk.CTkImage(Image.open(resource_path("icons/extract_cpk.png")), size=(40,40)),
    "extract_pac": ctk.CTkImage(Image.open(resource_path("icons/extract_pac.png")), size=(40,40)),
    "go_back": ctk.CTkImage(Image.open(resource_path("icons/go_back.png")), size=(20,20)),
}

# Open Button
open_file_button = ctk.CTkButton(app,
                     text="Open your .cpk or .pac archive file",
                     image=Icons["open_file"],
                     compound="top", # Icon above text
                     fg_color="transparent", # No color
                     hover_color=("gray85", "gray25"),
                     text_color="white",
                     width=50,
                     height=50,
                     command=open_file
 )
 
 
# Place at top-left
open_file_button.place(
    x=30,
    y=40
)

# Open Button
open_folder_button = ctk.CTkButton(app,
                     text="Open your output folder",
                     image=Icons["open_folder"],
                     compound="top", # Icon above text
                     fg_color="transparent", # No color
                     hover_color=("gray85", "gray25"),
                     text_color="white",
                     width=50,
                     height=50,
                     command=open_folder
 )
 
 
# Place at top-left
open_folder_button.place(
    x=60,
    y=240
)


def extract_cpk(): # Wrapper function
    archive_file = Dictionary["file_path"]
    output_folder = Dictionary["folder_path"]
    files = Dictionary["FilesToExtract"]
    
    
    parse_cpk_archive.Extract(files, archive_file, output_folder)
    

# Extract Button CPK
extract_cpk_button = ctk.CTkButton(app,
                     text="Extract your .cpk archive",
                     image=Icons["extract_cpk"],
                     compound="top", # Icon above text
                     fg_color="transparent", # No color
                     hover_color=("gray85", "gray25"),
                     text_color="white",
                     width=50,
                     height=50,
                     command=lambda: run_in_background(extract_cpk) # Use lambda to avoid calling the function
 )

# Place at top-left
extract_cpk_button.place(
    x=60,
    y=440
)



def extract_pac(): # Wrapper function
    archive_file = Dictionary["file_path"]
    output_folder = Dictionary["folder_path"]
    FilesToExtract = Dictionary["FilesToExtract"]
    
    pac.ExtractPACArchive(archive_file, output_folder, FilesToExtract)
    
   

# Extract Button PAC
extract_pac_button = ctk.CTkButton(app,
                     text="Extract your .pac archive",
                     image=Icons["extract_pac"],
                     compound="top", # Icon above text
                     fg_color="transparent", # No color
                     hover_color=("gray85", "gray25"),
                     text_color="white",
                     width=50,
                     height=50,
                     command=lambda: run_in_background(extract_pac)
 )

# Place at top-left
extract_pac_button.place(
    x=60,
    y=640
)

# Creator label
creator_label = ctk.CTkLabel(app, text="Created by haru233 on NexusMods, \nalso known by the username haruse31 on Discord, \nor haruse23 on GitHub.", font=("Helvetica", 14), text_color="grey")

creator_label.place(
    relx=0.02,
    rely=0.9,
    anchor="sw"
)                                


# Treeview Frame
right_frame = ctk.CTkFrame(app, width=1200, height=800)

right_frame.place(
    relx=0.25,
    rely=0.05,
    relwidth=0.73,
    relheight=0.9
)

right_frame.pack_propagate(False)

# Create Treeview object
tree = ttk.Treeview(
            right_frame,
            columns=("Directory Name", "Filename", "File Size", "Extract Size", "File Offset", "ContainsFilesOfType"),
            show="headings"
            )

# Set headings
tree.heading("Directory Name", text="Directory Name", anchor="w")
tree.heading("Filename", text="Filename", anchor="w")
tree.heading("File Size", text="File Size", anchor="w")
tree.heading("Extract Size", text="Extract Size", anchor="w")
tree.heading("File Offset", text="File Offset", anchor="w")
tree.heading("ContainsFilesOfType", text="File Types Contained Inside This PAC Archive", anchor="w")

# Set widths
tree.column("Directory Name", width=450)
tree.column("Filename", width=225)
tree.column("File Size", width=120)
tree.column("Extract Size", width=120)
tree.column("File Offset", width=120)
tree.column("ContainsFilesOfType", width=300)


# Add scrollbar
vertical_scrollbar = ttk.Scrollbar(
    right_frame,
    orient="vertical",
    command=tree.yview
)

horizontal_scrollbar = ttk.Scrollbar(
    right_frame,
    orient="horizontal",
    command=tree.xview
)

tree.configure(
    yscrollcommand=vertical_scrollbar.set,
    xscrollcommand=horizontal_scrollbar.set
)

# Packing
tree.grid(row=0, column=0, sticky="nsew")
vertical_scrollbar.grid(row=0, column=1, sticky="ns")
horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_columnconfigure(0, weight=1)


# Searchbox, the Entry (text/input box) with placeholder text
search_entry = ctk.CTkEntry(app, font=("Helvetica", 20), placeholder_text="Search...")

search_entry.place(
    relx=0.25,
    rely=0.001,
    relwidth=0.2,
    relheight=0.05
)

# Function to check searchbox against tree view files
def check(event):
    typed = search_entry.get()
    
    file_path = Dictionary["file_path"]
    
    files = Dictionary["FilesToExtract"]
    
    if typed == "":
        update_tree()
            
    else:
        output = []
        
        searchable_keys = [
            "DirName",
            "FileName",
            "FileSize",
            "ExtractSize",
            "FileOffset",
            "ContainsFilesOfType"
        ]
            

        for file in files:
            # Check only visible dictionary fields
            match = any(
                typed in str(file[key]).lower()
                for key in searchable_keys
                if key in file
            )
            
            if match:
                output.append(file)
            

        update_tree_on_search(output)






def update_tree_on_search(output):
    # Clear the tree
    tree.delete(*tree.get_children())
    
    ext = Dictionary["extension"]
    
    if ext == ".cpk":
        for file in output:
            tree.insert(
                "",
                "end",
                values=(
                    file["DirName"], # Directory Name
                    file["FileName"], # Filename
                    file["FileSize"], # File Size
                    file["ExtractSize"], # Extract Size
                    file["FileOffset"], # File Offset
                    "" # ContainsFilesOfType
                    
                )
            )
    
    else:
        for file in output:
            tree.insert(
                "",
                "end",
                values=(
                    "", # Directory Name
                    file["FileName"], # Filename
                    file["FileSize"], # File Size
                    "", # Extract Size
                    file["FileOffset"], # File Offset
                    file["ContainsFilesOfType"] # ContainsFilesOfType
                )
            )
    
    update_showing_label()

def get_selected_values(tree):
    selected_ids = tree.selection()  # Returns a tuple of selected item IDs

    # Get the selected rows's values
    if selected_ids:
        selected_items_values = []

        for item_id in selected_ids:
            item_data = tree.item(item_id)
            selected_items_values.append(item_data["values"])
        
        return selected_items_values
        
    return None  # Nothing is selected
    
    
def fillout(event):
    # Delete whatever is in the Entry box
    search_entry.delete(0, "end")
    
    selected_values = get_selected_values(tree)
    
    if selected_values:
        selected_value = selected_values[0]
    
        # Add clicked Treeview item to the Entry box
    
        search_entry.insert(0, selected_value[1]) # Filename
    
def on_double_click(event):
    item = tree.identify_row(event.y)
    if not item:
        return

    values = tree.item(item)["values"]

    filename = values[1] # FileName
    filetype = values[-1] # ContainsFilesOfType
    
    if filetype == "tex":
        view_texture()
    else:
        save_history()
        run_in_background(open_nested_archive_for_double_click, filename)



def open_nested_archive_for_double_click(filename):
    archive_path = Dictionary["ArchivePath"]
    
    if isinstance(archive_path, str): # Filepath
        source = open(archive_path, "rb")
        
    else: # BytesIO Object
        source = archive_path
        
    for file_dict in Dictionary["FilesToExtract"]:
        if file_dict["FileName"] == filename:
            
            file_offset = file_dict["FileOffset"]
            file_size = file_dict["FileSize"]
            
            source.seek(file_offset)
            fo = BytesIO(source.read(file_size)) # compressed file object (might not be compressed))
            
            if "ExtractSize" in file_dict: # If it has ExtractSize
                if file_dict["FileSize"] != file_dict["ExtractSize"]: # Decompress if it is compressed before parsing
                    cri_layla = crilayla.crilayla() # object from the class
            
                    cri_layla.ReadCrilayla(fo)
                    
                    fo = BytesIO(cri_layla.DecompressCrilayla())
                    
            
            parse_pac(fo)
            
            # Updating archive name and size labels
            app.after(0, lambda: update_archive_name_label(filename))
            
            app.after(0, lambda: update_archive_size_label( len(fo.getvalue()) ))
            
            
            
            break
    
    else:
        return


def show_context_menu(event):
    context_menu.delete(0, "end")
    
    item = tree.identify_row(event.y)

    if item:
        if item not in tree.selection():
            tree.selection_set(item)
            
           
        values = tree.item(item)["values"] # item values
        
        filetypes = values[-1] # ContainsFilesOfType
        
        if filetypes == "tex":
            context_menu.add_command(
                label="Extract Selected to the Output Folder",
                command=extract_selected
            )    
            
            context_menu.add_command(
                label="View Texture",
                command=view_texture
            )
            
            context_menu.add_command(
                label="Export to PNG",
                command=export_to_png
            )
            
        else:
            context_menu.add_command(
                label="Extract Selected to the Output Folder",
                command=extract_selected
            )    
            
        

        context_menu.post(event.x_root, event.y_root)

# Keybinding
tree.bind("<<TreeviewSelect>>", fillout)

search_entry.bind("<KeyRelease>", check)

tree.bind("<Double-1>", on_double_click)

tree.bind("<Button-3>", show_context_menu)

# Showing out of label
showing_label = ctk.CTkLabel(app, font=("Helvetica", 14), text_color="grey", text="Showing 0 out of 0 files", fg_color="transparent")

showing_label.place(
    relx=1.0,
    rely=1.0,
    anchor="se",
    x=-15,
    y=-10
)

def go_back():
    if tree_history:
        previous_item = tree_history.pop()
        
        
        
        
        # Clear current view
        for item in tree.get_children():
            tree.delete(item)

        # Restore previous view
        Dictionary["FilesToExtract"] = previous_item["FilesToExtract"]
        Dictionary["extension"] = previous_item["extension"]
        Dictionary["ArchiveName"] = previous_item["archive_name"]
        Dictionary["ArchiveSize"] = previous_item["archive_size"]
        
        
        update_tree()
            
            
        # Restore labels
        update_archive_name_label(Dictionary["ArchiveName"])
        update_archive_size_label(Dictionary["ArchiveSize"])
        update_archive_filecount_label()
        update_showing_label()

        
    else:
        # Updating archive name and size labels
        archive_name_label.configure(
            text=f"Archive Name: "
        )
        
        archive_size_label.configure(
            text=f"Archive Size: "
        )
        
        archive_filecount_label.configure(
            text=f"Archive FileCount: "
        )
        
        showing_label.configure(
            text=f"Showing 0 out of 0 files"
        )
        

back_button = ctk.CTkButton(app, text="Go Back", image=Icons["go_back"], command=go_back)

back_button.place(
    relx=0.88,
    rely=1.0,
    anchor="se",
    x=-15,
    y=-10
)


def extract_selected():
    items_values = get_selected_values(tree)
    
    FilesSelectedToExtract = []
    for item_values in items_values:
        filename = item_values[1] # Second element
        
        for file in Dictionary["FilesToExtract"]:
            if filename == file["FileName"]:
                FilesSelectedToExtract.append(file)
                
    
    archive_path = Dictionary["ArchivePath"]
    output_root = filedialog.askdirectory()
    
    if isinstance(archive_path, str): # Filepath
        source = open(archive_path, "rb")
        
    else: # BytesIO Object
        source = archive_path
        
       
    for file_selected in FilesSelectedToExtract:
        file_name = file_selected["FileName"]
        
        file_offset = file_selected["FileOffset"]
        file_size = file_selected["FileSize"]
        
        source.seek(file_offset)
        file_data = source.read(file_size)
    
    
    
        with open(f"{output_root}\\{file_name}", "wb") as out:
            out.write(file_data)
                
            
            
def view_texture():
    texture_objs = image_helper()[0] # texture
    imgs = image_helper()[1] # img
    
    # Display using system's default image viewer
    
    for img in imgs:
        img.show()
                    

def export_to_png():
    texture_objs = image_helper()[0] # texture
    imgs = image_helper()[1] # img
    
    output_root = filedialog.askdirectory()
    
    
    for img, texture_obj in zip(imgs, texture_objs):
        # Save as PNG
        img.save(f"{output_root}\\{texture_obj.TextureName}.png")
    
    
def image_helper():
    selected_rows = get_selected_values(tree)
    
    filenames = [selected_row[1] for selected_row in selected_rows] # Filename
    filetypes = [selected_row[-1] for selected_row in selected_rows] # ContainsFilesOfType
    
    texture_objs = []
    imgs = []
    
    archive_path = Dictionary["ArchivePath"]
    
    if isinstance(archive_path, str): # Filepath
        source = open(archive_path, "rb")
        
    else: # BytesIO Object
        source = archive_path

    for filetype, filename in zip(filetypes, filenames):
        if filetype == "tex":
            for file_dict in Dictionary["FilesToExtract"]:
                if filename == file_dict["FileName"]:
                
                    texture_offset = file_dict["FileOffset"]
                    texture_size = file_dict["FileSize"]
                    
                    source.seek(texture_offset)
                    texture_iobytes = BytesIO( source.read(texture_size) )
                    
                    texture_obj = texture.Texture()
                    
                    texture_obj.ParseTexture(texture_iobytes)
                    
                    texture_obj.DecodeBCn(7) #BC7
                
                    img = Image.fromarray(texture_obj.DecodedTexture)
                    
                    texture_objs.append(texture_obj)
                    imgs.append(img)
                    
    return texture_objs, imgs


# Create the context menu
context_menu = Menu(app, tearoff=0)



# Run the application
app.mainloop()