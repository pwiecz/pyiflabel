# -*- coding: utf-8 -*-
#
#       _imgfuncs.py
#
#       Copyright © 2012, 2013, 2014, 2018 Brandon Invergo <brandon@invergo.net>
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


from _binaryfuncs import read_char, read_long, read_short
from treatyofbabel.babelerrors import BabelImgError


class CoverImage(object):
    def __init__(self, data=None, img_format=None, width=None,
                 height=None, description=None):
        self.data = data
        self.img_format = img_format
        self.width = width
        self.height = height
        self.description = description


def get_jpeg_dim(img):
    if read_char(img, 0) != 0xff or read_char(img, 1) != 0xD8:
        raise BabelImgError("Data does not contain a JPEG image")
    dp = 2
    ep = len(img)
    while True:
        if dp > ep:
            raise BabelImgError("Invalid JPEG image")
        t1 = read_char(img, dp)
        dp += 1
        while t1 != 0xff:
            if dp > ep:
                raise BabelImgError("Invalid JPEG image")
            t1 = read_char(img, dp)
            dp += 1
        t1 = read_char(img, dp)
        dp += 1
        while t1 == 0xff:
            if dp > ep:
                raise BabelImgError("Invalid JPEG image")
            t1 = read_char(img, dp)
            dp += 1
        if t1 & 0xF0 == 0xC0 and not (t1 == 0xC4 or t1 == 0xC8 or t1 == 0xCC):
            dp += 3
            if dp > ep:
                raise BabelImgError("Invalid JPEG image")
            h = read_char(img, dp) * 2**8
            dp += 1
            if dp > ep:
                raise BabelImgError("Invalid JPEG image")
            h = h | read_char(img, dp)
            dp += 1
            if dp > ep:
                raise BabelImgError("Invalid JPEG image")
            w = read_char(img, dp) * 2**8
            dp += 1
            if dp > ep:
                raise BabelImgError("Invalid JPEG image")
            w = w | read_char(img, dp)
            return (w, h)
        elif t1 == 0xD8 or t1 == 0xD9:
            break
        else:
            if dp > ep:
                raise BabelImgError("Invalid JPEG image")
            l = read_char(img, dp) * 2**8
            dp += 1
            if dp > ep:
                raise BabelImgError("Invalid JPEG image")
            l = l | read_char(img, dp)
            l -= 2
            dp += l
            if dp > ep:
                raise BabelImgError("Invalid JPEG image")
    raise BabelImgError("Invalid JPEG image")


def get_png_dim(img):
    if (len(img) < 33):
        raise BabelImgError("Data does not contain a PNG image")
    header1 = [read_char(img, x) for x in range(8)]
    header2 = [read_char(img, 12+x) for x in range(4)]
    if ((header1 != [137, 80, 78, 71, 13, 10, 26, 10] or
         header2 != [ord(c) for c in ['I', 'H', 'D', 'R']])):
        raise BabelImgError("Data does not contain a PNG image")
    w = read_long(img, 16)
    h = read_long(img, 20)
    return (w, h)


def get_gif_dim(img):
    # Look for the "GIF" magic number
    header = [read_char(img, x) for x in range(3)]
    if header != [ord(c) for c in ['G', 'I', 'F']]:
        raise BabelImgError("Data does not contain a GIF image")
    header_len = 6
    logscreen_len = 7
    packed_field = read_char(img, header_len+4, '<')
    # The first bit of the packed field determines if there is a
    # Global Color Table
    global_color_tbl = packed_field & 0b10000000 == 0b10000000
    if global_color_tbl:
        # The last three bits determine the size of the GCT.
        # According to
        # http://giflib.sourceforge.net/whatsinagif/bits_and_bytes.html
        # This should be determined by the color resolution in bits
        # 2-4, however that doesn't seem to work.  This does
        gct_size = packed_field & 0b00000111
        # The Global Color Table uses 2^(N+1) bytes per color (RGB),
        # so 3*2^(N+1) bytes long
        gct_len = 3 * (2 ** (gct_size + 1))
    else:
        gct_len = 0
    # Check for a Graphics Control Extension block
    gce_offset = header_len + logscreen_len + gct_len
    gce_block = read_char(img, gce_offset, '<') == 0x21
    if gce_block:
        gce_len = 8
    else:
        gce_len = 0
    # Image Descriptior block
    img_descr_offset = gce_offset + gce_len
    if read_char(img, img_descr_offset, '<') != 0x2C:
        raise BabelImgError("Invalid GIF image")
    w = read_short(img, img_descr_offset+5, '<')
    h = read_short(img, img_descr_offset+7, '<')
    return (w, h)


def deduce_img_format(img):
    try:
        get_jpeg_dim(img)
    except BabelImgError:
        pass
    else:
        return "jpeg"
    try:
        get_png_dim(img)
    except BabelImgError:
        pass
    else:
        return "png"
    try:
        get_gif_dim(img)
    except BabelImgError:
        pass
    else:
        return "gif"
    return None
