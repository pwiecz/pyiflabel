# -*- coding: utf-8 -*-
#
#       quest.py
#
#       Copyright © 2012, 2013, 2014, 2015 Brandon Invergo <brandon@invergo.net>
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
import xml.dom.minidom
import zipfile
from cStringIO import StringIO
from binascii import hexlify

from treatyofbabel import ifiction
from treatyofbabel.babelerrors import BabelError


FORMAT = "quest"
FORMAT_EXT = [".quest"]
HOME_PAGE = "http://www.textadventures.co.uk"
HAS_COVER = False
HAS_META = True


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
    try:
        _extract_aslx(file_buffer)
    except:
        return False
    return True


def get_story_file_meta(file_buffer, truncate=False):
    aslx = _extract_aslx(file_buffer)
    aslx_dom = xml.dom.minidom.parseString(aslx)
    aslx_games = aslx_dom.getElementsByTagName("game")
    if len(aslx_games) == 0:
        raise BabelError("No game information found")
    aslx_game = aslx_games[0]
    gameinfo = ifiction.build_dict_from_node(aslx_game)
    ifiction_dom = ifiction.create_ifiction_dom()
    ifiction.add_comment(ifiction_dom,
                         "Bibliographic data translated from Quest ASLX")
    story_node = ifiction.add_story(ifiction_dom)
    title = aslx_game.getAttribute("name")
    ifid = gameinfo.get("gameid")
    ifiction.add_identification(ifiction_dom, story_node, [ifid], FORMAT)
    ifiction.add_bibliographic(
        ifiction_dom,
        story_node,
        truncate,
        title=title,
        author=gameinfo.get("author"),
        description=gameinfo.get("description"),
        genre=gameinfo.get("category")
        )
    return ifiction_dom.toprettyxml(indent="  ", encoding="UTF-8")


def get_story_file_cover(file_buffer):
    return None


def get_story_file_ifid(file_buffer):
    aslx = _extract_aslx(file_buffer)
    aslx_dom = xml.dom.minidom.parseString(aslx)
    aslx_games = aslx_dom.getElementsByTagName("game")
    if len(aslx_games) == 0:
        raise BabelError("No game information found")
    aslx_game = aslx_games[0]
    gameinfo = ifiction.build_dict_from_node(aslx_game)
    ifid = gameinfo.get("gameid")
    if ifid is None:
        file_hash = hexlify(md5.new(file_buffer).digest()).upper()
        ifid = "QUEST-{0}".format(file_hash)
    return ifid


def _extract_aslx(file_buffer):
    filelike = StringIO(str(file_buffer))
    filezip = zipfile.ZipFile(filelike)
    aslx_handle = filezip.open("game.aslx")
    aslx = aslx_handle.read()
    filelike.close()
    aslx_handle.close()
    return aslx
