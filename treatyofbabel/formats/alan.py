# -*- coding: utf-8 -*-
#
#       alan.py
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

from treatyofbabel.utils._binaryfuncs import read_long


FORMAT = "alan"
FORMAT_EXT = [".acd", ".a3c", ".a3r"]
HOME_PAGE = "http://www.alanif.se/"
HAS_COVER = False
HAS_META = False


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
    crc = 0
    if len(file_buffer) < 160:
        return False
    if not file_buffer.startswith('ALAN'):
        # Identify Alan 2.x
        bf = read_long(file_buffer, 4)
        if bf > len(file_buffer)/4:
            return False
        for i in range(24, 81, 4):
            if read_long(file_buffer, i) > len(file_buffer)/4:
                return False
        for i in range(160, bf * 4):
            crc += ord(file_buffer[i])
        if crc == read_long(file_buffer, 152):
            return True
    else:
        # Identify Alan 3.x
        crc = 0
        bf = read_long(file_buffer, 12)
        if bf > len(file_buffer)/4:
            return False
        for i in range(184, bf * 4):
            crc += ord(file_buffer[i])
        if crc == read_long(file_buffer, 176):
            return True
    return False


def get_story_file_meta(file_buffer, truncate=False):
    return None


def get_story_file_cover(file_buffer):
    return None


def get_story_file_ifid(file_buffer):
    file_hash = hexlify(md5.new(file_buffer).digest()).upper()
    return "ALAN-{0}".format(file_hash)
