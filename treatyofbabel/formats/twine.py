# -*- coding: utf-8 -*-
#
#       twine.py
#
#       Copyright © 2018 Brandon Invergo <brandon@invergo.net>
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
import md5
from binascii import hexlify

FORMAT = "twine"
FORMAT_EXT = [".html", ".htm"]
HOME_PAGE = "http://www.twinery.org"
HAS_COVER = False
HAS_META = False


def get_format_name():
    return FORMAT


def get_story_file_extension(file_buffer):
    if claim_story_file(file_buffer):
        return ".html"
    else:
        return None


def get_home_page():
    return HOME_PAGE


def get_file_extensions():
    return FORMAT_EXT


def claim_story_file(file_buffer):
    return "tw-story" in file_buffer


def get_story_file_meta(file_buffer, truncate=False):
    return None


def get_story_file_cover(file_buffer):
    return None


def get_story_file_ifid(file_buffer):
    m = re.search(r'ifid="([A-Za-z0-9-]+)"', file_buffer)
    if m is None:
        return hexlify(md5.new(file_buffer).digest()).upper()
    return m.group(1)
