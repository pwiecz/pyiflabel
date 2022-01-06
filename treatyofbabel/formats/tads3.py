# -*- coding: utf-8 -*-
#
#       tads3.py
#
#       Copyright © 2011, 2012, 2013, 2014, 2015, 2018 Brandon Invergo <brandon@invergo.net>
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
import md5
import os.path
from binascii import hexlify

from treatyofbabel.utils._binaryfuncs import read_int, read_short, read_byte
from treatyofbabel.utils._imgfuncs import CoverImage, get_jpeg_dim, get_png_dim
from treatyofbabel import ifiction
from treatyofbabel.babelerrors import BabelError


FORMAT = "tads3"
FORMAT_EXT = [".t3"]
HOME_PAGE = "http://www.tads.org"
HAS_COVER = True
HAS_META = True
T3_SIGNATURE = 'T3-image\015\012\032'
HTML_RES_ID = 'HTMLRES'
EOF_RES_ID = '$EOF'


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
    return file_buffer.startswith(T3_SIGNATURE)


def get_story_file_meta(file_buffer, truncate=False):
    gameinfo = _get_gameinfo(file_buffer)
    if gameinfo is None:
        return gameinfo
    authoremail = gameinfo.get("authoremail")
    if authoremail is not None:
        authors, emails = _parse_authors(authoremail)
    else:
        byline = gameinfo.get("byline")
        if byline is None:
            # TODO: raise a warning that there is insufficient metadata in the
            # gameinfo file (no author)
            return None
        authors, emails = _parse_authors(byline.strip("by "))
        if emails == "":
            emails = None
    ifiction_dom = ifiction.create_ifiction_dom()
    ifiction.add_comment(ifiction_dom, 
                         "Bibliographic data translated from TADS GameInfo")
    story_node = ifiction.add_story(ifiction_dom)
    ifid = gameinfo.get("ifid")
    if ifid is None:
        ifid = get_story_file_ifid(file_buffer)
    ifiction.add_identification(ifiction_dom, story_node, [ifid], FORMAT)
    ifiction.add_bibliographic(
        ifiction_dom,
        story_node,
        truncate,
        title=gameinfo.get("name"),
        author=authors,
        headline=gameinfo.get("headline"),
        description=gameinfo.get("desc"),
        genre=gameinfo.get("genre"),
        forgiveness=gameinfo.get("forgiveness"),
        series=gameinfo.get("series"),
        seriesnumber=gameinfo.get("seriesnumber"),
        language=gameinfo.get("language"),
        firstpublished=gameinfo.get("firstpublished")
        )
    url = gameinfo.get("url")
    if emails is not None or url is not None:
        ifiction.add_contact(ifiction_dom, story_node,
                              url=gameinfo.get("url"), email=emails)
    cover = get_story_file_cover(file_buffer)
    if cover is not None:
        ifiction.add_cover(ifiction_dom, story_node, cover.img_format,
                           cover.width, cover.height, cover.description)
    ifiction.add_format_info(
        ifiction_dom,
        story_node,
        "tads",
        version=gameinfo.get("version"),
        releasedate=gameinfo.get("releasedate"),
        presentationprofile=gameinfo.get("presentationprofile"),
        byline=gameinfo.get("byline")
        )
    return ifiction_dom.toprettyxml(indent="  ", encoding="UTF-8")


def get_story_file_cover(file_buffer):
    for resc_name in ['CoverArt.jpg', 'CoverArt.png']:
        cover_resc = _find_resource(file_buffer, resc_name)
        if cover_resc:
            ext = os.path.splitext(resc_name)[1].strip('.')
            if ext == 'jpg':
                (width, height) = get_jpeg_dim(cover_resc)
            else:
                (width, height) = get_png_dim(cover_resc)
            if width is None or height is None:
                raise BabelError("Image corrupted: cannot determine dimensions")
            cover = CoverImage(cover_resc, ext, width, height, None)
            return cover
    return None


def get_story_file_ifid(file_buffer):
    if not claim_story_file(file_buffer):
        return None
    gameinfo = _get_gameinfo(file_buffer)
    if gameinfo is None:
        return _calc_ifid(file_buffer)
    ifid = gameinfo.get("ifid")
    if ifid is None:
        return _calc_ifid(file_buffer)
    return ifid


def _calc_ifid(file_buffer):
    file_hash = hexlify(md5.new(file_buffer).digest()).upper()
    ifid = "TADS3-{0}".format(file_hash)
    return ifid


def _find_resource(file_buffer, name):
    name = name.lower()
    rsc_name_len = len(name)

    # Skip past TADS3 header (11 bytes signature, 2 bytes version, 32 bytes
    # reserved, 24 bytes timestamp
    p = 11 + 2 + 32 + 24
    while p < len(file_buffer):
        rsc_type = file_buffer[p:p + 4]
        block_size = read_int(file_buffer, p + 4, '<')
        if rsc_type == 'MRES':
            # Skip past the section block header
            p = p + 10
            block_start = p
            number_entries = read_short(file_buffer, p, '<')
            p = p + 2
            # Scan index entries
            for x in range(number_entries):
                rsc_offset = read_int(file_buffer, p, '<')
                rsc_size = read_int(file_buffer, p + 4, '<')
                name_len = read_byte(file_buffer, p + 8, '<')
                rsc_name = ''
                for xored_char in file_buffer[p + 9:p + 9 + rsc_name_len]:
                    rsc_name = rsc_name + chr(ord(xored_char) ^ 0xFF)
                if name_len == rsc_name_len and rsc_name.lower() == name:
                    return file_buffer[block_start + rsc_offset:
                                       block_start + rsc_offset + rsc_size]
                p = p + 9 + name_len
            p = block_start + block_size
        elif rsc_type == 'EOF':
            return None
        else:
            p = p + 10 + block_size
    return None


def _get_gameinfo(file_buffer):
    rsc = _find_resource(file_buffer, 'GameInfo.txt')
    if rsc is not None:
        #rsc = rsc.decode('utf-8')
        gameinfo = {}
        for line in rsc.split('\n'):
            line = line.strip()
            if not line.startswith('#'):
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip().lower()
                    value = parts[1].strip().replace('\\n', '\n')
                    value = _cleanup_info(value)
                    gameinfo[key] = value
        return gameinfo
    else:
        return None


def _cleanup_info(value):
    cleaned = re.sub('\s{2,}', ' ', value)
    return cleaned


def _parse_authors(author_str):
    author_list = []
    email_list = []
    author_split = author_str.split(';')
    for author in author_split:
        if '<' in author:
            name, email = author.split('<')
            email = email.strip()[:-1]
        else:
            name = author
            email = ""
        author_list.append(name.strip())
        email_list.append(email)
    if len(author_list) == 1:
        authors = author_list[0]
    elif len(author_list) == 2:
        authors = ' and '.join(authors)
    elif len(author_list) > 2:
        authors = ', '.join([', '.join(author_list[:-2]),
                             ' and '.join(author_list[-2:])])
    if len(email_list) == 1:
        emails = email_list[0]
    else:
        emails = ', '.join(email_list)
    return (authors, emails)
