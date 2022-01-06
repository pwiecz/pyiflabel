# -*- coding: utf-8 -*-
#
#       advsys.py
#
#       Copyright © 2012, 2013, 2014 Brandon Invergo <brandon@invergo.net>
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


FORMAT = "advsys"
FORMAT_EXT = [".dat"]
HOME_PAGE = "http://www.ifarchive.org/if-archive/programming/advsys/"
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
    if len(file_buffer) > 8:
        # bytes 2-8 contain the text "ADVSYS", unobfuscated by adding
        # 30 to each byte and then performing a bitwise NOT on it
        # since the Python NOT (~) operator works only on signed
        # (long) int values, producing negative values in this case,
        # we instead perform an XOR with 0xff.
        head = ''.join([chr((ord(a)+30) ^ 0xff) for a in file_buffer[2:8]])
        if head == "ADVSYS":
            return True
    return False


def get_story_file_meta(file_buffer, truncate=False):
    return None


def get_story_file_cover(file_buffer):
    return None


def get_story_file_ifid(file_buffer):
    file_hash = hexlify(md5.new(file_buffer).digest()).upper()
    return "ADVSYS-{0}".format(file_hash)
