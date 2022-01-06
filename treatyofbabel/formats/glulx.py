# -*- coding: utf-8 -*-
#
#       glulx.py
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

from treatyofbabel.utils._binaryfuncs import read_int, read_short


FORMAT = "glulx"
FORMAT_EXT = [".ulx"]
HOME_PAGE = "http://eblong.com/zarf/glulx"
HAS_COVER = False
HAS_META = False
INFORM_OFFSET = 36
MMAP_SIZE_OFFSET = 12
SERIAL_OFFSET = 54
CHECKSUM_OFFSET = 32
INFORM_IDENTIFIER = 'Info'
SERIAL_LENGTH = 6
RELEASE_NUMBER_OFFSET = 52


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
    return len(file_buffer) >= 256 and file_buffer.startswith('Glul')


def get_story_file_meta(file_buffer, truncate=False):
    return None


def get_story_file_cover(file_buffer):
    return None


def get_story_file_ifid(file_buffer):
    ifid_match = re.search('UUID://([^/]+)//', file_buffer)
    if ifid_match is not None:
        return ifid_match.group(1)
    else:
        is_inform = file_buffer[INFORM_OFFSET:INFORM_OFFSET +
                                len(INFORM_IDENTIFIER)] == INFORM_IDENTIFIER
        mmap_size = read_int(file_buffer, MMAP_SIZE_OFFSET)
        release_number = str(read_short(file_buffer, RELEASE_NUMBER_OFFSET))
        serial_number = re.sub('[^[[:alnum:]]]', '-',
                               file_buffer[SERIAL_OFFSET:SERIAL_OFFSET +
                                           SERIAL_LENGTH])
        checksum = read_int(file_buffer, CHECKSUM_OFFSET)
        if is_inform:
            ifid = "GLULX-{0}-{1}-{2:X}".format(release_number, serial_number,
                                                checksum)
        else:
            ifid = "GlULX-{0}-{1}".format(mmap_size, checksum)
        return ifid
