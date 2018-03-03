# snes_rom_info

![example screenshot](https://github.com/tetrismegistus/snes_rom_info/blob/master/rom_capture.png "Example Screenshot")

## Requirements

Should work with any standar Python 3 environments.

## Installation

You can just clone and run with python:

`$ git clone https://github.com/tetrismegistus/snes_rom_info
 $ cd snes_rom_info
 $ python3 snes_rom_info romname.smc`

Should you choose to download manually, please observe that hexview.py is required in the same directory snes_rom_info.py.

hexview.py also functions as a stand alone hexviewer:

`$ hexview.py filename`

and support arguments to view segments of a file, with -s specifying the starting address (in decimal), and -n the number of bytes:

`$ hexview.py -s 64 -n 128 filename`
