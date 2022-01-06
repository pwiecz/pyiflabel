# __init__.py ---

# Copyright (C) 2014, 2018 Brandon Invergo <brandon@invergo.net>

# Author: Brandon Invergo <brandon@invergo.net>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


"""This module provides functionality to discover information about
interactive fiction ("text adventure") story files.  It does this
according to the technical guidelines laid out in the Treaty of Babel
(http://babel.ifarchive.org).

The main functions for dealing with story files in a procedural manner
are contained directly in this module (treatyofbabel).  Functions for
creating and manipulating iFiction metadata files are contained in the
treatyofbabel.ifiction submodule.  Additionally, an object-oriented
means of representing story files is provided by the IFStory class in
the treatyofbabel.ifstory submodule.

The treatyofbabel.formats and treatyofbabel.wrappers submodules
provide low-level functions for handling individual story formats and
wrappers (e.g. blorb) and generally should not need to be directly
called.

"""


import os.path
import xml.dom.minidom

import ifiction
from babelerrors import BabelError
from formats import (adrift, advsys, agt, alan, executable, glulx,
                     hugo, level9, magscrolls, quest, tads2, tads3,
                     twine, zcode)
from wrappers import blorb

PYIFBABEL_VERSION = u"0.4"
TREATY_VERSION = u"9"
HANDLERS = [adrift, advsys, agt, alan, executable, glulx, hugo,
            level9, magscrolls, quest, tads2, tads3, twine, zcode]
EXTENSION_MAP = {}


for h in HANDLERS:
    for ext in h.get_file_extensions():
        EXTENSION_MAP[ext] = h


def deduce_handler(story_file, story_buffer):
    """Deduce the handler for a story file.

    Args:
        story_file: the file path of a story file
        story_buffer: a buffer containing the story file data
    Returns:
        The babel format/wrapper handler appropriate for the file
    Raises:
        ValueError: if story_file is None or empty
        BabelError: if the story is of an unknown format

    """
    if story_file is None or story_file == "":
        raise ValueError()
    basename = os.path.basename(story_file)
    extension = os.path.splitext(basename)[1]
    handler = EXTENSION_MAP.get(extension)
    if handler is None or not handler.claim_story_file(story_buffer):
        for h in HANDLERS:
            if h.claim_story_file(story_buffer):
                handler = h
                break
            else:
                handler = None
    if handler is None:
        raise BabelError("Unknown story format")
    return handler


def _get_story_data(story_file):
    """Extract the data from a story file.

    Args:
        story_file: the file path of a story file
    Returns:
        The data contained in the file
    Raises:
        ValueError: if story_file is None or empty or if the length of the data
        is unusually small

    """
    if story_file is None or story_file == "":
        raise ValueError("No story file specified")
    with open(story_file, 'rb') as story_handle:
        story_data = story_handle.read()
    # If the data read is less than 20 bytes (arbitrarily chosen), it probably
    # doesn't contain a valid story file.
    if len(story_data) < 20:
        raise ValueError("Truncated story file")
    return story_data


def deduce_format(story_file):
    """Deduce the format of a story file.

    Args:
        story_file: the file path of a story file
    Returns:
        The name of the formt of the story, which could be blorbed

    """
    story_data = _get_story_data(story_file)
    if blorb.claim_story_file(story_data):
        story_format = blorb.get_story_format(story_data)
        return "blorbed {0}".format(story_format)
    handler = deduce_handler(story_file, story_data)
    return handler.get_format_name()


def get_ifids(story_file):
    """Get the IFID from a story file or from an ifiction file.

    Args:
        story_file: the file path of a story file or an iFiction file
    Returns:
        A list of IFIDs associated with the file or None if the iFiction file
        is bogus

    """
    try:
        xml_doc = xml.dom.minidom.parse(story_file)
    except:
        story_data = _get_story_data(story_file)
        if blorb.claim_story_file(story_data):
            try:
                ifids = blorb.get_story_file_ifid(story_data)
            except:
                return [blorb._get_embedded_ifid(story_data)]
            else:
                return ifids
        handler = deduce_handler(story_file, story_data)
        return [handler.get_story_file_ifid(story_data)]
    else:
        if not ifiction.is_ifiction(xml_doc):
            return None
        ifids = []
        stories = ifiction.get_all_stories(xml_doc)
        for story in stories:
            ifids.append(ifiction.get_identification(story)["ifid"])
        return ifids


def get_meta(story_file, truncate=False):
    """Get the available metadata for a story file.

    Args:
        story_file: the file path of a story file
        truncate: truncate the metadata fields to 240 characters (2400
                  characters for the description) (default: False)
    Returns:
        An iFiction metadata file or None if the story's format does not
        provide metadata

    """
    story_data = _get_story_data(story_file)
    if blorb.claim_story_file(story_data):
        return blorb.get_story_file_meta(story_data)
    else:
        handler = deduce_handler(story_file, story_data)
        if handler.HAS_META:
            return handler.get_story_file_meta(story_data, truncate)
    return None


def get_cover(story_file):
    """Extract cover art from a story file.

    Args:
        story_file: the file path of a story file
    Returns:
        A CoverImage object containing the cover data (see
        treatyofbabel.utils._imgfuncs) or None if the story does not have a
        cover associated with it

    """
    story_data = _get_story_data(story_file)
    if blorb.claim_story_file(story_data):
        return blorb.get_story_file_cover(story_data)
    else:
        handler = deduce_handler(story_file, story_data)
        if handler.HAS_COVER:
            return handler.get_story_file_cover(story_data)
    return None


def get_story(story_file):
    """Extract a story from a story file, particularly a wrapped (blorbed)
    file.

    Args:
        story_file: the file path of a story file
    Returns:
        The data of the (wrapped) story file

    """
    story_data = _get_story_data(story_file)
    if blorb.claim_story_file(story_data):
        return blorb.get_story_file(story_data)
    else:
        return story_data


def verify_ifiction(ifiction_file):
    """Verify the integrity of an iFiction file. (Not yet implemented)

    Args:
        ifiction_file: the file path of an iFiction file
    Returns:
        True if the file is correct, False otherwise

    """
    pass


def ifiction_lint(ifiction_file):
    """Verify the style of an iFiction file. (Not yet implemented)

    Args:
        ifiction_file: the file path of an iFiction file
    Returns:
        True if the file has good style, False otherwise

    """
    pass


def complete_ifiction(ifiction_file):
    """Generate a complete iFiction file from a sparse one. (Not yet
    implemented)

    Args:
        ifiction_file: the file path of an iFiction file
    Returns:
        A completed iFiction file

    """
    pass


def make_blorb(output_file, story_file, ifiction_file,
               coverart_file=None):
    """Bundle story file and ifiction into a blorb.

    Args:
        output_file: the blorb file to write
        story_file: the file path of a story file
        ifiction_file: the file path of an iFiction file
        coverart_file: the file path of a PNG or JPEG cover art file
                       (default: None)
    Returns:
        No return value

    """
    story_format = deduce_format(story_file)
    blorb.create(output_file, story_file, story_format, ifiction_file,
                 coverart_file)
