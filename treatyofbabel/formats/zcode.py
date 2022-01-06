# -*- coding: utf-8 -*-
#
#       zcode.py
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


FORMAT = "zcode"
FORMAT_EXT = [".z{0}".format(v) for v in range(3, 9)]
HOME_PAGE = "http://www.inform-fiction.org"
HAS_COVER = False
HAS_META = False
HEADER_LENGTH = 0x3C
STORY_START = 0x40
RELEASE_NUMBER_OFFSET = 0x02
SERIAL_OFFSET = 0x12
SERIAL_LENGTH = 6
CHECKSUM_OFFSET = 0x1C
CHECKSUM_LENGTH = 2
UUID_HEADER = 'UUID://'


def get_format_name():
    return FORMAT


def get_story_file_extension(file_buffer):
    if claim_story_file(file_buffer):
        version = file_buffer[0]
        return ".z{0}".format(version)
    else:
        return None


def get_home_page():
    return HOME_PAGE


def get_file_extensions():
    return FORMAT_EXT


def claim_story_file(file_buffer):
    if (len(file_buffer) < HEADER_LENGTH or
            ord(file_buffer[0]) < 1 or
            ord(file_buffer[0]) > 8):
        return False
    else:
        for i in range(4, 15, 2):
            j = _read_zint(file_buffer, i)
            if j > len(file_buffer) or j < STORY_START:
                return False
        return True


def get_story_file_meta(file_buffer, truncate=False):
    return None


def get_story_file_cover(file_buffer):
    return None


def get_story_file_ifid(file_buffer):
    if len(file_buffer) < 0x1D:
        return None
    serial_number = file_buffer[SERIAL_OFFSET:SERIAL_OFFSET + SERIAL_LENGTH]
    release_number = _read_zint(file_buffer, RELEASE_NUMBER_OFFSET)
    checksum = file_buffer[CHECKSUM_OFFSET:CHECKSUM_OFFSET + CHECKSUM_LENGTH]
    checksum = hexlify(checksum).upper()
    v0 = serial_number[0]
    v1 = serial_number[1]
    is_vintage = (v0 == '8' or v0 == '9' or (v0 == '0' and v1 >= '0'
                                             and v1 <= '5'))
    if not is_vintage:
        uuid_start = file_buffer.find(UUID_HEADER)
        if (uuid_start >= 0 and
                len(file_buffer) > uuid_start + len(UUID_HEADER)):
            uuid_end = file_buffer.find('/', uuid_start + len(UUID_HEADER))
            if uuid_end >= 0:
                return file_buffer[uuid_start + len(UUID_HEADER):uuid_end]
    ifid = ''.join(['ZCODE-', str(release_number), '-', serial_number])
    if serial_number[0] != '8' and serial_number != '000000':
        ifid = ''.join([ifid, '-', checksum])
    return ifid


def _read_zint(file_buffer, i):
    return ord(file_buffer[i]) * 256 + ord(file_buffer[i + 1])
