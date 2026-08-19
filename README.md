# CALL-to-EXIST-Tool
Game archive file explorer for Tokyo Ghoul: re [CALL to EXIST]

[NexusMods Page](https://www.nexusmods.com/tokyoghoulrecalltoexist/mods/1)

# Compiling
I used Nuitka to compile the program, you can compile the gui.py in onefile mode using this CMD command and it will produce a single independent .exe file:

`python -m nuitka --onefile --enable-plugin=tk-inter --include-package=customtkinter --include-package=imagecodecs --include-package-data=imagecodecs --include-data-dir=icons=icons --output-filename="CALL to EXIST Tool" --windows-icon-from-ico=icons\app.ico gui.py`

# Credits & References
`For the cpk archive files format and encryption of the packets:`
[CPK](https://github.com/mosamadeeb/CriPakTools/blob/asbr/LibCPK/CPK.cs)



`For the CRILAYLA decompression logic:`
[CRILAYLA](https://github.com/kamikat/cpktools/blob/master/cpk/crilayla.py)


`All the others credited in any of those two github repositories are included.`
