# -*- coding: utf-8 -*-
#
#       level9.py
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


FORMAT = "level9"
FORMAT_EXT = [".l9", ".sna"]
HOME_PAGE = "http://www.if-legends.org/~l9memorial/html/home.html"
HAS_COVER = False
HAS_META = False
L9_REGISTRY = [
    (0x3a31, 0xe5, "LEVEL9-001-1"),
    (0x8333, 0xb7, "LEVEL9-001-1"),
    (0x7c6f, 0x0f, "LEVEL9-001-1"),
    (0x72fa, 0x8b, "LEVEL9-001-1"),
    (0x38dd, 0x31, "LEVEL9-001-A"),
    (0x39c0, 0x44, "LEVEL9-001-B"),
    (0x3a12, 0x8f, "LEVEL9-001-C"),
    (0x37f1, 0x77, "LEVEL9-001-2"),
    (0x844d, 0x50, "LEVEL9-001-2"),
    (0x738e, 0x5b, "LEVEL9-001-2"),
    (0x3900, 0x1c, "LEVEL9-001-3"),
    (0x8251, 0x5f, "LEVEL9-001-3"),
    (0x7375, 0xe5, "LEVEL9-001-3"),
    (0x3910, 0xac, "LEVEL9-001-4"),
    (0x7a78, 0x5e, "LEVEL9-001-4"),
    (0x78d5, 0xe3, "LEVEL9-001-4"),
    (0x3ad6, 0xa7, "LEVEL9-001-5"),
    (0x38a5, 0x0f, "LEVEL9-001-6"),
    (0x361e, 0x7e, "LEVEL9-001-7"),
    (0x3934, 0x75, "LEVEL9-001-8"),
    (0x3511, 0xcc, "LEVEL9-001-9"),
    (0x593a, 0xaf, "LEVEL9-002-1"),
    (0x7931, 0xb9, "LEVEL9-002-1"),
    (0x6841, 0x4a, "LEVEL9-002-1"),
    (0x57e6, 0x8a, "LEVEL9-002-2"),
    (0x7cdf, 0xa5, "LEVEL9-002-2"),
    (0x6bc0, 0x62, "LEVEL9-002-2"),
    (0x5819, 0xcd, "LEVEL9-002-3"),
    (0x7a0c, 0x97, "LEVEL9-002-3"),
    (0x692c, 0x21, "LEVEL9-002-3"),
    (0x579b, 0xad, "LEVEL9-002-4"),
    (0x7883, 0xe2, "LEVEL9-002-4"),
    (0x670a, 0x94, "LEVEL9-002-4"),
    (0x5323, 0xb7, "LEVEL9-003"),
    (0x6e60, 0x83, "LEVEL9-003"),
    (0x5b58, 0x50, "LEVEL9-003"),
    (0x63b6, 0x2e, "LEVEL9-003"),
    (0x6968, 0x32, "LEVEL9-003"),
    (0x5b50, 0x66, "LEVEL9-003"),
    (0x6970, 0xd6, "LEVEL9-003"),
    (0x5ace, 0x11, "LEVEL9-003"),
    (0x6e5c, 0xf6, "LEVEL9-003"),
    (0x1929, 0x00, "LEVEL9-004-DEMO"),
    (0x40e0, 0x02, "LEVEL9-004-DEMO"),
    (0x3ebb, 0x00, "LEVEL9-004-en"),
    (0x3e4f, 0x00, "LEVEL9-004-en"),
    (0x3e8f, 0x00, "LEVEL9-004-en"),
    (0x0fd8, 0x00, "LEVEL9-004-en"),
    (0x14a3, 0x00, "LEVEL9-004-en"),
    (0x110f, 0x00, "LEVEL9-004-fr"),
    (0x4872, 0x00, "LEVEL9-004-de"),
    (0x4846, 0x00, "LEVEL9-004-de"),
    (0x11f5, 0x00, "LEVEL9-004-de"),
    (0x11f5, 0x00, "LEVEL9-004-de"),
    (0x76f4, 0x5e, "LEVEL9-005"),
    (0x5b16, 0x3b, "LEVEL9-005"),
    (0x6c8e, 0xb6, "LEVEL9-005"),
    (0x6f4d, 0xcb, "LEVEL9-005"),
    (0x6f6a, 0xa5, "LEVEL9-005"),
    (0x5e31, 0x7c, "LEVEL9-005"),
    (0x6f70, 0x40, "LEVEL9-005"),
    (0x6f6e, 0x78, "LEVEL9-005"),
    (0x5a8e, 0xf2, "LEVEL9-005"),
    (0x76f4, 0x5a, "LEVEL9-005"),
    (0x630e, 0x8d, "LEVEL9-006"),
    (0x630e, 0xbe, "LEVEL9-006"),
    (0x6f0c, 0x95, "LEVEL9-006"),
    (0x593a, 0x80, "LEVEL9-006"),
    (0x6bd2, 0x65, "LEVEL9-006"),
    (0x6dc0, 0x63, "LEVEL9-006"),
    (0x58a6, 0x24, "LEVEL9-006"),
    (0x6de8, 0x4c, "LEVEL9-006"),
    (0x58a3, 0x38, "LEVEL9-006"),
    (0x63be, 0xd6, "LEVEL9-007"),
    (0x378c, 0x8d, "LEVEL9-007"),
    (0x63be, 0x0a, "LEVEL9-007"),
    (0x34b3, 0x20, "LEVEL9-008"),
    (0x34b3, 0xc7, "LEVEL9-008"),
    (0x34b3, 0x53, "LEVEL9-008"),
    (0xb1a9, 0x80, "LEVEL9-009-1"),
    (0x908e, 0x0d, "LEVEL9-009-1"),
    (0xad41, 0xa8, "LEVEL9-009-1"),
    (0xb1aa, 0xad, "LEVEL9-009-1"),
    (0x8aab, 0xc0, "LEVEL9-009-1"),
    (0xb0ec, 0xc2, "LEVEL9-009-1"),
    (0xb19e, 0x92, "LEVEL9-009-1"),
    (0x5ff0, 0xf8, "LEVEL9-009-1"),
    (0x52aa, 0xdf, "LEVEL9-009-1"),
    (0xab9d, 0x31, "LEVEL9-009-2"),
    (0x8f6f, 0x0a, "LEVEL9-009-2"),
    (0xa735, 0xf7, "LEVEL9-009-2"),
    (0xab8b, 0xbf, "LEVEL9-009-2"),
    (0x8ac8, 0x9a, "LEVEL9-009-2"),
    (0xaf82, 0x83, "LEVEL9-009-2"),
    (0x6024, 0x01, "LEVEL9-009-2"),
    (0x6ffa, 0xdb, "LEVEL9-009-2"),
    (0xae28, 0x87, "LEVEL9-009-3"),
    (0x9060, 0xbb, "LEVEL9-009-3"),
    (0xa9c0, 0x9e, "LEVEL9-009-3"),
    (0xae16, 0x81, "LEVEL9-009-3"),
    (0x8a93, 0x4f, "LEVEL9-009-3"),
    (0xb3e6, 0xab, "LEVEL9-009-3"),
    (0x6036, 0x3d, "LEVEL9-009-3"),
    (0x723a, 0x69, "LEVEL9-009-3"),
    (0xd188, 0x13, "LEVEL9-010-1"),
    (0x9089, 0xce, "LEVEL9-010-1"),
    (0xb770, 0x03, "LEVEL9-010-1"),
    (0xd19b, 0xad, "LEVEL9-010-1"),
    (0x8ab7, 0x68, "LEVEL9-010-1"),
    (0xd183, 0x83, "LEVEL9-010-1"),
    (0x5a38, 0xf7, "LEVEL9-010-1"),
    (0x76a0, 0x3a, "LEVEL9-010-1"),
    (0xc594, 0x03, "LEVEL9-010-2"),
    (0x908d, 0x80, "LEVEL9-010-2"),
    (0xb741, 0xb6, "LEVEL9-010-2"),
    (0xc5a5, 0xfe, "LEVEL9-010-2"),
    (0x8b1e, 0x84, "LEVEL9-010-2"),
    (0xc58f, 0x65, "LEVEL9-010-2"),
    (0x531a, 0xed, "LEVEL9-010-2"),
    (0x7674, 0x0b, "LEVEL9-010-2"),
    (0xd79f, 0xb5, "LEVEL9-010-3"),
    (0x909e, 0x9f, "LEVEL9-010-3"),
    (0xb791, 0xa1, "LEVEL9-010-3"),
    (0xd7ae, 0x9e, "LEVEL9-010-3"),
    (0x8b1c, 0xa8, "LEVEL9-010-3"),
    (0xd79a, 0x57, "LEVEL9-010-3"),
    (0x57e4, 0x19, "LEVEL9-010-3"),
    (0x765e, 0xba, "LEVEL9-010-3"),
    (0xbb93, 0x36, "LEVEL9-011-1"),
    (0x898a, 0x43, "LEVEL9-011-1"),
    (0x8970, 0x6b, "LEVEL9-011-1"),
    (0xbb6e, 0xa6, "LEVEL9-011-1"),
    (0x86d0, 0xb7, "LEVEL9-011-1"),
    (0xbb6e, 0xad, "LEVEL9-011-1"),
    (0x46ec, 0x64, "LEVEL9-011-1"),
    (0x74e0, 0x92, "LEVEL9-011-1"),
    (0xc58e, 0x4a, "LEVEL9-011-2"),
    (0x8b9f, 0x61, "LEVEL9-011-2"),
    (0x8b90, 0x4e, "LEVEL9-011-2"),
    (0xc58e, 0x43, "LEVEL9-011-2"),
    (0x8885, 0x22, "LEVEL9-011-2"),
    (0x6140, 0x18, "LEVEL9-011-2"),
    (0x6dbc, 0x97, "LEVEL9-011-2"),
    (0xcb9a, 0x0f, "LEVEL9-011-3"),
    (0x8af9, 0x61, "LEVEL9-011-3"),
    (0x8aea, 0x4e, "LEVEL9-011-3"),
    (0xcb9a, 0x08, "LEVEL9-011-3"),
    (0x87e5, 0x0e, "LEVEL9-011-3"),
    (0x640e, 0xc1, "LEVEL9-011-3"),
    (0x7402, 0x07, "LEVEL9-011-3"),
    (0xbba4, 0x94, "LEVEL9-012-1"),
    (0xc0cf, 0x4e, "LEVEL9-012-1"),
    (0x8afc, 0x07, "LEVEL9-012-1"),
    (0x8feb, 0xba, "LEVEL9-012-1"),
    (0xb4c9, 0x94, "LEVEL9-012-1"),
    (0xc0bd, 0x57, "LEVEL9-012-1"),
    (0x8ade, 0xf2, "LEVEL9-012-1"),
    (0x4fd2, 0x9d, "LEVEL9-012-1"),
    (0x5c7a, 0x44, "LEVEL9-012-1"),
    (0x768c, 0xe8, "LEVEL9-012-1"),
    (0xd0c0, 0x56, "LEVEL9-012-2"),
    (0xd5e9, 0x6a, "LEVEL9-012-2"),
    (0x8aec, 0x13, "LEVEL9-012-2"),
    (0x8f6b, 0xfa, "LEVEL9-012-2"),
    (0xb729, 0x51, "LEVEL9-012-2"),
    (0xd5d7, 0x99, "LEVEL9-012-2"),
    (0x8b0e, 0xfb, "LEVEL9-012-2"),
    (0x4dac, 0xa8, "LEVEL9-012-2"),
    (0x53a2, 0x1e, "LEVEL9-012-2"),
    (0x76b0, 0x1d, "LEVEL9-012-2"),
    (0xb6ac, 0xc6, "LEVEL9-012-3"),
    (0xbb8f, 0x1a, "LEVEL9-012-3"),
    (0x8aba, 0x0d, "LEVEL9-012-3"),
    (0x8f71, 0x2f, "LEVEL9-012-3"),
    (0xb702, 0xe4, "LEVEL9-012-3"),
    (0xbb7d, 0x17, "LEVEL9-012-3"),
    (0x8ab3, 0xc1, "LEVEL9-012-3"),
    (0x4f96, 0x22, "LEVEL9-012-3"),
    (0x5914, 0x22, "LEVEL9-012-3"),
    (0x765e, 0x4f, "LEVEL9-012-3"),
    (0x5eb9, 0x30, "LEVEL9-013"),
    (0x5eb9, 0x5d, "LEVEL9-013"),
    (0x5eb9, 0x6e, "LEVEL9-013"),
    (0xb257, 0xf8, "LEVEL9-013"),
    (0xb576, 0x2a, "LEVEL9-013"),
    (0x8d78, 0x3a, "LEVEL9-013"),
    (0x9070, 0x43, "LEVEL9-013"),
    (0xb38c, 0x37, "LEVEL9-013"),
    (0xb563, 0x6a, "LEVEL9-013"),
    (0xb57c, 0x44, "LEVEL9-013"),
    (0xb260, 0xe5, "LEVEL9-013"),
    (0x8950, 0xa1, "LEVEL9-013"),
    (0xb579, 0x89, "LEVEL9-013"),
    (0x579e, 0x97, "LEVEL9-013"),
    (0x69fe, 0x56, "LEVEL9-013"),
    (0x6f1e, 0xda, "LEVEL9-013"),
    (0x5671, 0xbc, "LEVEL9-014"),
    (0x6fc6, 0x14, "LEVEL9-014"),
    (0x5aa4, 0xc1, "LEVEL9-014"),
    (0x7410, 0x5e, "LEVEL9-014"),
    (0x5aa4, 0xc1, "LEVEL9-014"),
    (0x5aa4, 0xc1, "LEVEL9-014"),
    (0xb797, 0x1f, "LEVEL9-014"),
    (0xbaca, 0x3a, "LEVEL9-014"),
    (0x8c46, 0xf0, "LEVEL9-014"),
    (0x8f51, 0xb2, "LEVEL9-014"),
    (0xb451, 0xa8, "LEVEL9-014"),
    (0xbab2, 0x87, "LEVEL9-014"),
    (0xbac7, 0x7f, "LEVEL9-014"),
    (0xb7a0, 0x7e, "LEVEL9-014"),
    (0x8a60, 0x2a, "LEVEL9-014"),
    (0xbac4, 0x80, "LEVEL9-014"),
    (0x579a, 0x2a, "LEVEL9-014"),
    (0x5a50, 0xa9, "LEVEL9-014"),
    (0x6108, 0xdd, "LEVEL9-014"),
    (0x506c, 0xf0, "LEVEL9-015"),
    (0x505d, 0x32, "LEVEL9-015"),
    (0xa398, 0x82, "LEVEL9-015"),
    (0xa692, 0xd1, "LEVEL9-015"),
    (0x8d56, 0xd3, "LEVEL9-015"),
    (0x903f, 0x6b, "LEVEL9-015"),
    (0xa4e2, 0xa6, "LEVEL9-015"),
    (0xa67c, 0xb8, "LEVEL9-015"),
    (0xa69e, 0x6c, "LEVEL9-015"),
    (0xa3a4, 0xdf, "LEVEL9-015"),
    (0x8813, 0x11, "LEVEL9-015"),
    (0xa698, 0x41, "LEVEL9-015"),
    (0x5500, 0x50, "LEVEL9-015"),
    (0x6888, 0x8d, "LEVEL9-015"),
    (0x6da0, 0xb8, "LEVEL9-015"),
    (0x6064, 0xbd, "LEVEL9-016"),
    (0x6064, 0x01, "LEVEL9-016"),
    (0x6047, 0x6c, "LEVEL9-016"),
    (0x6064, 0xda, "LEVEL9-016"),
    (0x6064, 0x95, "LEVEL9-016"),
    (0x60c4, 0x28, "LEVEL9-016"),
    (0x5cb7, 0xfe, "LEVEL9-016"),
    (0x5ca1, 0x33, "LEVEL9-016"),
    (0x5cb7, 0x64, "LEVEL9-016"),
    (0x7d16, 0xe6, "LEVEL9-016"),
    (0x639c, 0x8b, "LEVEL9-016"),
    (0x60f7, 0x68, "LEVEL9-016"),
    (0x772f, 0xca, "LEVEL9-016"),
    (0x7cff, 0xf8, "LEVEL9-016"),
    (0x7cf8, 0x24, "LEVEL9-016"),
    (0x7d14, 0xe8, "LEVEL9-016"),
    (0x7c55, 0x18, "LEVEL9-016"),
    (0x5f43, 0xca, "LEVEL9-016"),
    (0xc132, 0x14, "LEVEL9-017-1"),
    (0xbeab, 0x2d, "LEVEL9-017-1"),
    (0x9058, 0xcf, "LEVEL9-017-1"),
    (0xbe94, 0xcc, "LEVEL9-017-1"),
    (0x8a21, 0xf4, "LEVEL9-017-1"),
    (0x55ce, 0xa1, "LEVEL9-017-1"),
    (0x5cbc, 0xa5, "LEVEL9-017-1"),
    (0x762e, 0x82, "LEVEL9-017-1"),
    (0x99bd, 0x65, "LEVEL9-017-2"),
    (0x8f43, 0xc9, "LEVEL9-017-2"),
    (0x8a12, 0xe3, "LEVEL9-017-2"),
    (0x54a6, 0xa9, "LEVEL9-017-2"),
    (0x5932, 0x4e, "LEVEL9-017-2"),
    (0x5bd6, 0x35, "LEVEL9-017-2"),
    (0xbcb6, 0x7a, "LEVEL9-017-3 (Amiga/PC/ST)"),
    (0x90ac, 0x68, "LEVEL9-017-3"),
    (0x8a16, 0xcc, "LEVEL9-017-3"),
    (0x51bc, 0xe3, "LEVEL9-017-3"),
    (0x5860, 0x95, "LEVEL9-017-3"),
    (0x6fa8, 0xa4, "LEVEL9-017-3"),
    (0x5fab, 0x5c, "LEVEL9-018"),
    (0x5fab, 0x2f, "LEVEL9-018"),
    (0x7b31, 0x6e, "LEVEL9-018"),
    (0x67a3, 0x9d, "LEVEL9-018"),
    (0x6bf8, 0x3f, "LEVEL9-018"),
    (0x7363, 0x65, "LEVEL9-018"),
    (0x7b2f, 0x70, "LEVEL9-018"),
    (0x7b2f, 0x70, "LEVEL9-018"),
    (0x6541, 0x02, "LEVEL9-018"),
    (0x5834, 0x42, "LEVEL9-019-1"),
    (0x765d, 0xcd, "LEVEL9-019-1"),
    (0x6ce5, 0x58, "LEVEL9-019-1"),
    (0x56dd, 0x51, "LEVEL9-019-2"),
    (0x6e58, 0x07, "LEVEL9-019-2"),
    (0x68da, 0xc1, "LEVEL9-019-2"),
    (0x5801, 0x53, "LEVEL9-019-3"),
    (0x7e98, 0x6a, "LEVEL9-019-3"),
    (0x6c67, 0x9a, "LEVEL9-019-3"),
    (0x54a4, 0x01, "LEVEL9-019-4"),
    (0x81e2, 0xd5, "LEVEL9-019-4"),
    (0x6d91, 0xb9, "LEVEL9-019-4"),
    (0x5828, 0xbd, "LEVEL9-020"),
    (0x6d84, 0xf9, "LEVEL9-020"),
    (0x6d84, 0xc8, "LEVEL9-020"),
    (0x6030, 0x47, "LEVEL9-020"),
    (0x772b, 0xcd, "LEVEL9-020"),
    (0x546c, 0xb7, "LEVEL9-020"),
    (0x7cd9, 0x0c, "LEVEL9-020"),
    (0x60dd, 0xf2, "LEVEL9-020"),
    (0x6161, 0xf3, "LEVEL9-020"),
    (0x788d, 0x72, "LEVEL9-020"),
    (0x7cd7, 0x0e, "LEVEL9-020"),
    (0x5ebb, 0xf1, "LEVEL9-020")]


def get_format_name():
    return FORMAT


def get_story_file_extension(file_buffer):
    # this is wrong...need to figure out which files are .l9 and which are .sna
    if claim_story_file(file_buffer):
        return FORMAT_EXT[0]
    else:
        return None


def get_home_page():
    return HOME_PAGE


def get_file_extensions():
    return FORMAT_EXT


def claim_story_file(file_buffer):
    (version, ifid) = _get_l9_version(file_buffer)
    if version > 0:
        if ifid is not None:
            return True
    return False


def get_story_file_meta(file_buffer, truncate=False):
    return None


def get_story_file_cover(file_buffer):
    return None


def get_story_file_ifid(file_buffer):
    (version, ifid) = _get_l9_version(file_buffer)
    if version == 0:
        return None
    if ifid is not None:
        return ifid
    file_hash = hexlify(md5.new(file_buffer).digest()).upper()
    return 'LEVEL9-{0}-{1}'.format(version, file_hash)


def _read_l9_int(file_buffer, i):
    return ord(file_buffer[i+1]) * 2**8 + ord(file_buffer[i])


def _v2_recognition(file_buffer):
    for i in range(len(file_buffer) - 20):
        if (_read_l9_int(file_buffer, i + 4) == 0x0020 and
                _read_l9_int(file_buffer, i + 10) == 0x8000 and
                _read_l9_int(file_buffer, i + 20) == _read_l9_int(file_buffer,
                                                                  i + 22)):
            length = _read_l9_int(file_buffer, i + 28)
            if length and length + i <= len(file_buffer):
                c = 0
                for j in range(length + 1):
                    c += ord(file_buffer[i + j])
                return (2, length, c % 256)
    return (0, None, None)


def _v1_recognition(file_buffer):
    a = 0xff
    b = 0xff
    i = 0
    while i < len(file_buffer) - 20:
        if file_buffer[i:i + 5] == 'ATTAC' and ord(file_buffer[i + 5]) == 0xcb:
            a = ord(file_buffer[i + 6])
            break
        i += 1
    while i < len(file_buffer) - 20:
        if file_buffer[i:i + 4] == 'BUNC' and ord(file_buffer[i + 4]) == 0xc8:
            b = ord(file_buffer[i + 5])
            break
        i += 1
    if a is 0xff and b is 0xff:
        return (0, None)
    if a == 0x14 and b == 0xff:
        return (1, 'LEVEL9-006')
    elif a == 0x15 and b == 0x5d:
        return (1, 'LEVEL9-013')
    elif a == 0x1a and b == 0x24:
        return (1, 'LEVEL9-005')
    elif a == 0x20 and b == 0x3b:
        return (1, 'LEVEL9-003')
    return (1, None)


def _v3_recognition_phase(phase, file_buffer):
    ll = 0
    extent = len(file_buffer)
    for i in range(extent - 20):
        if ll:
            break
        length = _read_l9_int(file_buffer, i)
        end = length + i
        if phase != 3:
            if (end < (extent - 2) and
                ((phase == 2 or
                  ((ord(file_buffer[end - 1]) == 0 and
                    ord(file_buffer[end - 2]) == 0) or
                   (ord(file_buffer[end + 1]) == 0 and
                    ord(file_buffer[end + 2]) == 0))) and
                 length > 0x4000 and length <= 0xdb00)):
                if length != 0 and ord(file_buffer[i + 13]) == 0:
                    for j in range(i, i + 16, 2):
                        i0 = _read_l9_int(file_buffer, j)
                        i2 = _read_l9_int(file_buffer, j + 2)
                        i4 = _read_l9_int(file_buffer, j + 4)
                        if i0 + i2 == i4 and i0 + i2:
                            ll += 1
        else:
            i2 = _read_l9_int(file_buffer, i + 2)
            i4 = _read_l9_int(file_buffer, i + 4)
            i6 = _read_l9_int(file_buffer, i + 6)
            i8 = _read_l9_int(file_buffer, i + 8)
            i10 = _read_l9_int(file_buffer, i + 10)
            if (extent > 0x0fd0 and end <= (extent - 2) and
                ((i2 + i4) == i6 and i2 != 0 and i4 != 0) and
                ((i6 + i8) == i10 and
                 (ord(file_buffer[i + 18]) == 0x2a or
                  ord(file_buffer[i + 18]) == 0x2c) and
                 ord(file_buffer[i + 19]) == 0 and
                 ord(file_buffer[i + 20]) == 0 and
                 ord(file_buffer[i + 21]) == 0)):
                ll = 2
        if ll > 1:
            c = 0
            if phase == 3:
                ll = 1
            else:
                c = ord(file_buffer[end])
                checksum = 0
                for j in range(i, end+1):
                    checksum += ord(file_buffer[j])
                if not checksum % 256:
                    ll = 1
                else:
                    ll = 0
        else:
            ll = 0
    if ll != 0:
        if length < 0x8500:
            return (3, length, c)
        else:
            return (4, length, c)
    return (0, None, None)


def _get_l9_ifid(length, c):
    for story in L9_REGISTRY:
        if length == story[0] and c == story[1]:
            return story[2]
    return None


def _get_l9_version(file_buffer):
    ret, length, c = _v2_recognition(file_buffer)
    if ret > 0:
        ifid = _get_l9_ifid(length, c)
        return (2, ifid)
    ret, length, c = _v3_recognition_phase(1, file_buffer)
    if ret > 0:
        ifid = _get_l9_ifid(length, c)
        return (ret, ifid)
    ret, ifid = _v1_recognition(file_buffer)
    if ret > 0:
        return (1, ifid)
    ret, length, c = _v3_recognition_phase(2,  file_buffer)
    if ret > 0:
        ifid = _get_l9_ifid(length, c)
        return ret
    ret, length, c = _v3_recognition_phase(3, file_buffer)
    return (ret, None)
