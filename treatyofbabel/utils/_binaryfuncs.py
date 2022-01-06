# -*- coding: utf-8 -*-
#
#       binary_funcs.py
#
#       Copyright © 2011, 2012, 2013, 2014 Brandon Invergo <brandon@invergo.net>
#       Copyright © 2009, 2010 Per Liedman <per@liedman.net>
#
#       This file is part of Grotesque.
#
#       Grotesque is free software: you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation, either version 3 of the License, or
#       (at your option) any later version.
#
#       Grotesque is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with Grotesque.  If not, see <http://www.gnu.org/licenses/>.


import struct


def read_int(file_buffer, offset, endian_char='>'):
    return struct.unpack_from('{0}I'.format(endian_char),
                              file_buffer, offset)[0]


def read_short(file_buffer, offset, endian_char='>'):
    return struct.unpack_from('{0}H'.format(endian_char),
                              file_buffer, offset)[0]


def read_byte(file_buffer, offset, endian_char='>'):
    return struct.unpack_from('{0}B'.format(endian_char),
                              file_buffer, offset)[0]


def read_long(file_buffer, offset, endian_char='>'):
    return struct.unpack_from('{0}L'.format(endian_char),
                              file_buffer, offset)[0]


def read_char(file_buffer, offset, endian_char='>'):
    return struct.unpack_from('{0}B'.format(endian_char),
                              file_buffer, offset)[0]
