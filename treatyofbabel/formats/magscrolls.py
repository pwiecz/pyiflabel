# -*- coding: utf-8 -*-
#
#       magscrolls.py
#
#       Copyright © 2011, 2012, 2013, 2014 Brandon Invergo <brandon@invergo.net>
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


FORMAT = "magscrolls"
FORMAT_EXT = [".mag"]
HOME_PAGE = "http://www.if-legends.org/~msmemorial/memorial.htm"
HAS_COVER = False
HAS_META = False
MANIFEST = [
    {'gv': 0,
     'header': ''.join(['\000\000\000\000\000\000\000\000\000\000',
                        '\000\000\000\000\000\000\000\000\000\000']),
     'title': 'The Pawn',
     'bafn': 0,
     'year': 1985,
     'ifid': 'MAGNETIC-1',
     'author': 'Rob Steggles'},
    {'gv': 1,
     'header': ''.join(['\000\004\000\001\007\370\000\000\340\000',
                        '\000\000\041\064\000\000\040\160\000\000']),
     'title': 'Guild of Thieves',
     'bafn': 0,
     'year': 1987,
     'ifid': 'MAGNETIC-2',
     'author': 'Rob Steggles'},
    {'gv': 2,
     'header': ''.join(['\000\000\000\000\000\000\000\000\000\000',
                        '\000\000\000\000\000\000\000\000\000\000']),
     'title': 'Jinxter',
     'bafn': 0,
     'year': 1987,
     'ifid': 'MAGNETIC-3',
     'author': 'Georgina Sinclair and Michael Bywater'},
    {'gv': 4,
     'header': ''.join(['\000\004\000\001\045\140\000\001\000\000',
                        '\000\000\161\017\000\000\035\210\000\001']),
     'title': 'Corruption',
     'bafn': 0,
     'year': 1988,
     'ifid': 'MAGNETIC-4',
     'author': 'Rob Steggles and Hugh Steers'},
    {'gv': 4,
     'header': ''.join(['\000\004\000\001\044\304\000\001\000\000',
                        '\000\000\134\137\000\000\040\230\000\001']),
     'title': 'Fish!',
     'bafn': 0,
     'year': 1988,
     'ifid': 'MAGNETIC-5',
     'author': 'John Molloy, Pete Kemp, Phil South, Rob Steggles'},
    {'gv': 4,
     'header': ''.join(['\000\003\000\000\377\000\000\000\340\000',
                        '\000\000\221\000\000\000\036\000\000\001']),
     'title': 'Corruption',
     'bafn': 0,
     'year': 1988,
     'ifid': 'MAGNETIC-4',
     'author': 'Rob Steggles and Hugh Steers'},
    {'gv': 4,
     'header': ''.join(['\000\003\000\001\000\000\000\000\340\000',
                        '\000\000\175\000\000\000\037\000\000\001']),
     'title': 'Fish!',
     'bafn': 0,
     'year': 1988,
     'ifid': 'MAGNETIC-5',
     'author': 'John Molloy, Pete Kemp, Phil South, Rob Steggles'},
    {'gv': 4,
     'header': ''.join(['\000\003\000\000\335\000\000\000\140\000',
                        '\000\000\064\000\000\000\023\000\000\000']),
     'title': 'Myth',
     'bafn': 0,
     'year': 1989,
     'ifid': 'MAGNETIC-6',
     'author': 'Paul Findley'},
    {'gv': 4,
     'header': ''.join(['\000\004\000\001\122\074\000\001\000\000',
                        '\000\000\114\146\000\000\057\240\000\001']),
     'title': 'Wonderland',
     'bafn': 0,
     'year': 1990,
     'ifid': 'MAGNETIC-7',
     'author': 'David Bishop'}]


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
    if len(file_buffer) < 42 or not file_buffer.startswith('MaSc'):
        return False
    return True


def get_story_file_meta(file_buffer, truncate=False):
    return None


def get_story_file_cover(file_buffer):
    return None


def get_story_file_ifid(file_buffer):
    if len(file_buffer) < 42:
        return None
    for story in MANIFEST:
        if ((file_buffer[13] < 3 and story['gv'] == file_buffer[13]) or
                (story['header'] == file_buffer[12:32])):
            return story['ifid']
    file_hash = hexlify(md5.new(file_buffer).digest()).upper()
    return "MAGNETIC-{0}".format(file_hash)
