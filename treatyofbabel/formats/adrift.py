# -*- coding: utf-8 -*-
#
#       adrift.py
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


from binascii import hexlify
import md5


FORMAT = "adrift"
FORMAT_EXT = [".taf"]
HOME_PAGE = "http://www.adrift.org.uk"
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
    if len(file_buffer) < 12:
        return False
    else:
        decoder = _AdriftDecoder()
        decoded_header = ''.join([decoder.decode(c) for c in file_buffer[0:7]])
        return decoded_header == 'Version'


def get_story_file_meta(file_buffer, truncate=False):
    return None


def get_story_file_cover(file_buffer):
    return None


def get_story_file_ifid(file_buffer):
    decoder = _AdriftDecoder()
    decoder.skip(8)
    ifid = 'ADRIFT-'
    ifid = ''.join([ifid, decoder.decode(file_buffer[8])])
    decoder.skip(1)
    ifid = ''.join([ifid, decoder.decode(file_buffer[10])])
    ifid = ''.join([ifid, decoder.decode(file_buffer[11])])
    ifid = ''.join([ifid, '-'])
    ifid = ''.join([ifid,  hexlify(md5.new(file_buffer).digest()).upper()])
    return ifid


class _AdriftDecoder:
    INITIAL_STATE = 0x00A09E86
    SCRAMBLE1 = 0x43FD43FD
    SCRAMBLE2 = 0x00C39EC3
    SCRAMBLE3 = 0x00FFFFFF

    def __init__(self):
        self.state = _AdriftDecoder.INITIAL_STATE

    def decode(self, character):
        self.state = (self.state * _AdriftDecoder.SCRAMBLE1 +
                      _AdriftDecoder.SCRAMBLE2) & _AdriftDecoder.SCRAMBLE3
        r = 255 * self.state / (_AdriftDecoder.SCRAMBLE3 + 1)
        return chr(r ^ ord(character))

    def skip(self, number_bytes):
        for x in range(0, number_bytes):
            self.decode('x')
