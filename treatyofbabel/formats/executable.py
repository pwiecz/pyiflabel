# -*- coding: utf-8 -*-
#
#       executable.py
#
#       Copyright © 2011, 2012, 2013, 2014, 2018 Brandon Invergo <brandon@invergo.net>
#
#       This file is part of pyifbabel.
#
#       pyifbabel is free software: you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation, either version 3 of the License, or
#       (at your option) any later version.
#
#       pyifbabel is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with pyifbabel.  If not, see <http://www.gnu.org/licenses/>.


import md5
from binascii import hexlify
from treatyofbabel.utils._binaryfuncs import read_short


FORMAT = "executable"
FORMAT_EXT = [".exe"]
HOME_PAGE = "http://http://en.wikipedia.org/wiki/Executable"
HAS_COVER = False
HAS_META = False
ELFMAGIC = ''.join([chr(x) for x in [0x7f, 0x45, 0x4c, 0x46]])
JAVAMAGIC = ''.join([chr(x) for x in [0xCA, 0xFE, 0xBA, 0xBE]])
AMIGAMAGIC = ''.join([chr(x) for x in [0, 0, 3, 0xe7]])
MACHOMAGIC = ''.join([chr(x) for x in [0xFE, 0xED, 0xFA, 0xCE]])
EXETYPES = [("MZ", "MZ", 2),
            (ELFMAGIC, "ELF", 4),
            (JAVAMAGIC, "JAVA", 4),
            (AMIGAMAGIC, "AMIGA", 4),
            ("#! ", "SCRIPT", 3),
            (MACHOMAGIC, "MACHO", 4),
            ("APPL", "MAC", 4)]


def get_format_name():
    return FORMAT


def get_story_file_extension(file_buffer):
    if claim_story_file(file_buffer):
        return FORMAT_EXT[0]
    else:
        return None


def get_home_page():
    return HOME_PAGE


def get_file_extensions():
    return FORMAT_EXT


def claim_story_file(file_buffer):
    if _deduce_magic(file_buffer):
        return True
    return False


def get_story_file_meta(file_buffer, truncate=False):
    return None


def get_story_file_cover(file_buffer):
    return None


def get_story_file_ifid(file_buffer):
    magic = _deduce_magic(file_buffer)
    if magic is None:
        return None
    file_hash = hexlify(md5.new(file_buffer).digest()).upper()
    return '-'.join([magic, file_hash])


def _deduce_magic(file_buffer):
    for magic, name, length in EXETYPES:
        if len(file_buffer) >= length and magic == file_buffer[0:length]:
            return name
    return None

def is_win32_executable(file_buffer):
    if _deduce_magic(file_buffer) != "MZ":
        return False
    lfanew = file_buffer[60:62]
    offset = read_short(file_buffer, 60, "<")
    if offset > len(file_buffer) - 3:
        return False
    return file_buffer[offset:offset+2] == "PE"
