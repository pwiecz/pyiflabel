# -*- coding: utf-8 -*-
#
#       blorb.py
#
#       Copyright © 2011, 2012, 2013, 2014, 2015, 2018 Brandon Invergo <brandon@invergo.net>
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


from ctypes import create_string_buffer
import os
import struct

from treatyofbabel.utils._binaryfuncs import read_int
from treatyofbabel.utils._imgfuncs import CoverImage, get_jpeg_dim, get_png_dim
from treatyofbabel.utils._imgfuncs import deduce_img_format
from treatyofbabel import ifiction
from treatyofbabel.babelerrors import BabelError

FORMAT = "blorb"
FORMAT_EXT = [".blorb", ".blb", ".zblorb", ".zlb", ".gblorb", ".glb"]
HOME_PAGE = "http://eblong.com/zarf/blorb"


def get_format_name():
    return FORMAT


def get_story_file_extension(file_buffer):
    if claim_story_file(file_buffer):
        story_format = get_story_format(file_buffer)
        if story_format == "zcode":
            return FORMAT_EXT[2]
        elif story_format == "glulx":
            return FORMAT_EXT[4]
        else:
            return FORMAT_EXT[0]
    return None


def get_home_page():
    return HOME_PAGE


def get_file_extensions():
    return FORMAT_EXT


def claim_story_file(file_buffer):
    if len(file_buffer) < 16 or not file_buffer.startswith("FORM") \
            or file_buffer[8:12] != "IFRS":
        return False
    return True


def get_story_file_meta(file_buffer, truncate=False):
    index, length = _get_chunk(file_buffer, "IFmd")
    if index is None:
        return None
    return file_buffer[index:index + length]


def get_story_file_cover(file_buffer):
    i, length = _get_chunk(file_buffer, "Fspc")
    if length < 4:
        return None
    i = read_int(file_buffer, i)
    pict_i, pict_len = _get_resource(file_buffer, "Pict", i)
    if pict_i is None:
        return None
    description = _get_resource_description(file_buffer, "Pict", i)
    cover_data = file_buffer[pict_i:pict_i + pict_len]
    cover_format = file_buffer[pict_i - 8:pict_i - 4]
    if cover_format[:3] == "PNG":
        ext = "png"
        (width, height) = get_png_dim(cover_data)
    elif cover_format == "JPEG":
        ext = "jpg"
        (width, height) = get_jpeg_dim(cover_data)
    else:
        raise BabelError("Unsupported image format")
    cover = CoverImage(cover_data, ext, width, height, description)
    return cover


def get_story_file_ifid(file_buffer):
    meta = get_story_file_meta(file_buffer)
    if meta is None:
        return [_get_embedded_ifid(file_buffer)]
    story_dom = ifiction.get_ifiction_dom(meta)
    story = ifiction.get_all_stories(story_dom)[0]
    ident = ifiction.get_identification(story)
    ifid_list = ident.get("ifid_list")
    if ifid_list is None or len(ifid_list) == 0:
        return [_get_embedded_ifid(file_buffer)]
    return ifid_list


def get_story_file(file_buffer):
    index, length = _get_resource(file_buffer, "Exec", 0)
    if index is None:
        return None
    return file_buffer[index:index + length]


def get_story_format(file_buffer):
    treaty_registry = {"ZCOD": "zcode", "GLUL": "glulx", "TAD2": "tads2",
                       "TAD3": "tads3", "HUGO": "hugo", "ALAN": "alan",
                       "ADRI": "adrift", "LEVE": "level9", "AGT": "agt",
                       "MAGS": "magscrolls", "ADVS": "advsys",
                       "EXEC": "executable"}
    for story_format in treaty_registry:
        index, length = _get_chunk(file_buffer, story_format)
        if index is not None:
            return treaty_registry.get(story_format)
    return None


def create(out_file, story_file, story_format, ifiction_file=None,
           coverart_file=None):
    treaty_registry = {"zcode": "ZCOD", "glulx": "GLUL", "tads2": "TAD2",
                       "tads3": "TAD3", "hugo": "HUGO", "alan": "ALAN",
                       "adrift": "ADRI", "level9": "LEVE", "agt": "AGT",
                       "magscrolls": "MAGS", "advsys": "ADVS",
                       "executable": "EXEC"}
    story_len = os.path.getsize(story_file)
    frmt = treaty_registry.get(story_format)
    if frmt is None:
        raise BabelError("Unsupported story format")
    if coverart_file is not None:
        cover_len = os.path.getsize(coverart_file)
        ridx_num = 2
        with open(coverart_file) as h:
            image_data = h.read()
            cover_frmt = deduce_img_format(image_data)
        if cover_frmt is None:
            raise BabelError("Unsupported or broken image format")
        elif cover_frmt == "png":
            cover_frmt = "PNG "
        else:
            cover_frmt = "JPEG"
    else:
        cover_len = 0
        ridx_num = 1
    # RIdx: 4 byte resource count + 12 bytes per resource descriptor
    ridx_len = 4 + ridx_num * 12
    # Insert the story file after 12 byte FORM header, 12 byte RIdx
    # header, and all 12 byte resource descriptors
    story_start = 24 + ridx_num * 12
    # The total length (in the FORM header chunk) is: 4 byte IFRS identifier
    total_len = 4
    #   + 8 byte RIdx header + RIdx length
    total_len += 8 + ridx_len
    #   + 8 byte EXEC header + story file length [+ pad byte]
    total_len += 8 + story_len + (story_len % 2)
    if ifiction_file is not None:
        if_len = os.path.getsize(ifiction_file)
        if_chunk = (("4c", "IFmd"), ("L", if_len), ("file", ifiction_file))
        # Total length increased by:
        #   + 8 byte IFmd header + ifiction length [+ pad byte]
        total_len += 8 + if_len + (if_len % 2)
    if coverart_file is not None:
        # Insert the cover file after the story and the 8 byte JPEG/PNG header
        cover_start = story_start + story_len + 8
        # The cover_chunk RIdx entry has already been counted in the
        # total_len above (via ridx_len)
        cover_chunk = (("4c", "Pict"), ("L", 1), ("L", cover_start))
        cover_file_chunk = (("4c", cover_frmt), ("L", cover_len),
                            ("file", coverart_file))
        fspc_chunk = (("4c", "Fspc"), ("L", 4), ("L", 1))
        # Total length increased by:
        #     + 8 byte PNG/JPEG header + image length [+ pad byte]
        total_len += 8 + cover_len + (cover_len % 2)
        #     + 12 byte Fspc headerp
        total_len += 12
    else:
        cover_chunk = None
        cover_file_chunk = None
        fspc_chunk = None
    chunks = [(("4c", "FORM"), ("L", total_len), ("4c", "IFRS")),
              (("4c", "RIdx"), ("L", ridx_len), ("L", ridx_num)),
              (("4c", "Exec"), ("L", 0), ("L", story_start)),
              cover_chunk,
              (("4c", frmt), ("L", story_len), ("file", story_file)),
              cover_file_chunk,
              fspc_chunk,
              if_chunk]
    with open(out_file, 'wb') as h:
        for chunk in chunks:
            _write_chunk(h, chunk)


def _write_chunk(handle, chunk):
    if chunk is None or not chunk:
        return
    for fmt, data in chunk:
        if fmt == "file":
            with open(data, 'rb') as h:
                data_bytes = h.read()
        elif fmt == "4c":
            data_bytes = struct.pack(">{0}".format(fmt), data[0],
                                     data[1], data[2], data[3])
        else:
            data_bytes = struct.pack(">{0}".format(fmt), data)
        handle.write(data_bytes)
        if len(data_bytes) % 2:
            handle.write(struct.pack(">c", '\0'))


def _get_embedded_ifid(file_buffer):
    story_file = get_story_file(file_buffer)
    story_format = get_story_format(file_buffer)
    if story_format == "zcode":
        from treatyofbabel.formats import zcode as handler
    elif story_format == "glulx":
        from treatyofbabel.formats import glulx as handler
    elif story_format == "tads2":
        from treatyofbabel.formats import tads2 as handler
    elif story_format == "tads3":
        from treatyofbabel.formats import tads3 as handler
    elif story_format == "hugo":
        from treatyofbabel.formats import tads3 as handler
    elif story_format == "alan":
        from treatyofbabel.formats import tads3 as handler
    elif story_format == "adrift":
        from treatyofbabel.formats import tads3 as handler
    elif story_format == "level9":
        from treatyofbabel.formats import level9 as handler
    elif story_format == "agt":
        from treatyofbabel.formats import agt as handler
    elif story_format == "magscrolls":
        from treatyofbabel.formats import magscrolls as handler
    elif story_format == "advsys":
        from treatyofbabel.formats import advsys as handler
    elif story_format == "executable":
        from treatyofbabel.formats import executable as handler
    else:
        raise BabelError("Unknown story format")
    return handler.get_story_file_ifid(story_file)


def _get_chunk(file_buffer, chunk_id):
    i = 12
    while i < len(file_buffer) - 8:
        length = read_int(file_buffer, i + 4)
        if file_buffer[i:i + 4] == chunk_id:
            if length > file_buffer:
                return (None, None)
            return (i + 8, length)
        if length % 2 != 0:
            length = length + 1
        i = i + length + 8
    return (None, None)


def _get_resource(file_buffer, resource, n):
    r, length = _get_chunk(file_buffer, "RIdx")
    if r is None:
        return (None, None)
    ridx = file_buffer[r+4:]
    ridx_len = read_int(file_buffer, r)
    for i in range(ridx_len):
        if (ridx[i * 12:i * 12 + 4] == resource and
                read_int(ridx, i * 12 + 4) == n):
            j = i
            i = read_int(ridx, j * 12 + 8)
            begin = i + 8
            out_len = read_int(file_buffer, i + 4)
            return (begin, out_len)
    return (None, None)


def _get_resources(file_buffer):
    index, length = _get_chunk("RIdx")
    number_resources = read_int(index, 0)
    result = []
    for i in xrange(0, number_resources):
        rsc_name = index[4 + i * 12:8 + i * 12]
        rsc_number = read_int(index, 8 + i * 12)
        result.append((rsc_name, rsc_number))
    return result


def _get_resource_description(file_buffer, resource, n):
    r, length = _get_chunk(file_buffer, "RDes")
    if r is None:
        return None
    rdes = file_buffer[r+4:]
    rdes_len = read_int(file_buffer, r)
    n = 0
    b = 0
    while n < rdes_len:
        res_usage = rdes[b:b+4]
        res_num = read_int(rdes, b+4)
        res_len = read_int(rdes, b+8)
        if res_usage == resource and res_num == n:
            text_start = b + 12
            text = rdes[text_start:text_start+length]
            return text
        b += 12 + res_len
    return None
