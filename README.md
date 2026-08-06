# CALL-to-EXIST-Tool
Game archive file explorer for Tokyo Ghoul: re [CALL to EXIST]


# Compiling
I used Nuitka to compile the program, you can compile the gui.py in onefile mode using this CMD command:

`python -m nuitka --onefile --enable-plugin=tk-inter --include-package=customtkinter --include-package=imagecodecs --include-package-data=imagecodecs --include-data-dir=icons=icons --output-filename="CALL to EXIST Tool" --windows-icon-from-ico=icons\app.ico gui.py`
