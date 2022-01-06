# -*- coding: utf-8 -*-
#
#       agt.py
#
#       Copyright © 2011, 2012, 2013, 2014 Brandon Invergo <brandon@invergo.net>
#       
#       This file is part of pyifbabel.
#
#       pyifbabel is free software: you can redistribute it and/or
#       modify it under the terms of the GNU General Public License as
#       published by the Free Software Foundation, either version 3 of
#       the License, or (at your option) any later version.
#
#       pyifbabel is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with pyifbabel.  If not, see <http://www.gnu.org/licenses/>.


import struct

from treatyofbabel.utils._binaryfuncs import read_short, read_int


FORMAT = "agt"
FORMAT_EXT = [".agx"]
HOME_PAGE = "http://www.ifarchive.org/indexes/if-archiveXprogrammingXagt"
HAS_COVER = False
HAS_META = False
AGX_MAGIC = (0x58, 0xC7, 0xC1, 0x51)


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
    header = struct.unpack_from('<BBBB', file_buffer, 0)
    if (len(file_buffer) < 36 or header != AGX_MAGIC):
        return False
    return True


def get_story_file_meta(file_buffer, truncate=False):
    return None


def get_story_file_cover(file_buffer):
    return None


def get_story_file_ifid(file_buffer):
    length = read_int(file_buffer, 32, '<')
    if len(file_buffer) < length + 6:
        return None
    game_version = read_short(file_buffer, length, '<')
    game_sig = read_int(file_buffer, length + 2, '<')
    return 'AGT-{0:05d}-{1:08X}'.format(game_version, game_sig)
