#!/usr/bin/env python
"""
This script automates the workflow for generating an updated Crocdb database
"""
import os
from make import make
from scripts.download_gametdb_xmls import download_gametdb_xmls
from scripts.download_libretro_dats import download_libretro_dats
from scripts.download_mame_hashes import download_mame_hashes

if __name__ == '__main__':
    # Change directory to script location
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    download_gametdb_xmls()
    download_libretro_dats()
    download_mame_hashes()
    make()
