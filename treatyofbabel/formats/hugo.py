# -*- coding: utf-8 -*-
#
#       hugo.py
#
#       Copyright © 2011, 2012, 2013, 2014 Brandon Invergo <brandon@invergo.net>
#       Copyright © 2009, 2010 Per Liedman <per@liedman.net>
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


import re

from treatyofbabel.utils._binaryfuncs import read_char


FORMAT = "hugo"
FORMAT_EXT = [".hex"]
HOME_PAGE = "http://www.generalcoffee.com"
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
    if file_buffer is None or len(file_buffer) < 40:
        return False
    if ord(file_buffer[0]) < 34:
        scale = 4
    else:
        scale = 16
    for i in range(3, 11):
        if ord(file_buffer[i]) < 32 or ord(file_buffer[i]) > 126:
            return False
    for i in range(11, 24, 2):
        if _read_hugo_addx(file_buffer, i) * scale > len(file_buffer):
            return False
    return True


def get_story_file_meta(file_buffer, truncate=False):
    return None


def get_story_file_cover(file_buffer):
    return None


def get_story_file_ifid(file_buffer):
    if len(file_buffer) < 11:
        return None
    ifid_match = re.search('UUID://([^/]+)//', file_buffer)
    if ifid_match is not None:
        return ifid_match.group(1)
    serial = file_buffer[3:11]
    serial = re.sub('\W', '-', serial)
    ifid = 'HUGO-{0:d}-{1:02X}-{2:02X}-{3}'.format(read_char(file_buffer, 0),
                                                   read_char(file_buffer, 1),
                                                   read_char(file_buffer, 2),
                                                   serial)
    return ifid


def _read_hugo_addx(file_buffer, i):
    return ord(file_buffer[i]) + ord(file_buffer[i + 1]) * 2**8
