# -*- coding: utf-8 -*-
#
#       ifstory.py
#
#       Copyright © 2012, 2013, 2014, 2015, 2018 Brandon Invergo <brandon@invergo.net>
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


"""This module provides the IFStory class, which implements an object-oriented
means of working with interactive fiction stories and the Treaty of Babel
bibliographical data standard.  In addition, the class provides some handy
extra functions for retrieving bibliographical data from online sources.

"""


import os.path
from urllib2 import urlopen
import time

import ifiction
import treatyofbabel
from utils._imgfuncs import CoverImage, get_png_dim, get_jpeg_dim, get_gif_dim, deduce_img_format
from babelerrors import IFictionError, BabelError
from treatyofbabel import PYIFBABEL_VERSION


class StrictDict(dict):
    """A derivative of the dict class whose legal keys must be declared at
    initialization.

    Additionally, all values must be coercible to a given type.

    """
    def __init__(self, value_type, **kwargs):
        super(StrictDict, self).__init__(**kwargs)
        self._value_type = value_type

    def __setitem__(self, i, y):
        if i not in self:
            raise KeyError
        try:
            value = self._value_type(y)
        except:
            raise ValueError
        super(StrictDict, self).__setitem__(i, value)


class IFStory(object):
    """A class storing interactive fiction bibliographical data.

    """
    def __init__(self, story_file=None, ific_story_node=None):
        """Initialize the object.

        Args:
            story_file: the story file
            ific_story_node: an IFiction Node containing the story's
                             bibliographical data

        """
        self.story_file = story_file
        self.ifid_list = []
        self.format = u""
        self.bafn = u""
        self.bibliographic = StrictDict(
            unicode, title=u"", author=u"", language=u"", headline=u"",
            firstpublished=u"", genre=u"", group=u"", forgiveness=u"",
            description=u"", series=u"", seriesnumber=u"")
        self.resources = []
        self.contacts = StrictDict(unicode, url=u"", email=u"")
        self.cover = CoverImage()
        self.format_info = {}
        self.releases = []
        self.colophon = StrictDict(unicode, generator=u"",
                                   generatorversion=u"",
                                   originated=u"")
        self.annotation = {}
        if ific_story_node is not None:
            self.load_from_ifiction(ific_story_node)
        elif story_file is not None:
            self.load_from_story_file(story_file)

    def add_resource(self, filename, description):
        """Add a resource to the story.

        Args:
            filename: the resource's file name
            description: the resource's description

        """
        filename = os.path.basename(filename)
        self.resources.append((filename, description))

    def remove_resource(self, filename):
        """Remove a resource.

        Args:
            filename: the file name of the resource to remove

        """
        filename = os.path.basename(filename)
        for resource in self.resources:
            if resource[0] == filename:
                self.resources.remove(resource)
                break

    def add_release(self, releasedate, version=u"", compiler=u"",
                    compilerversion=u"", attached=False):
        """Add a release for the story.

        Args:
            releasedate: the date the story was released
            version: the version identifier for the story
            compiler: the compiler used to create the story
            compilerversion: the version identifier of the compiler
            attached: True if the story file is attached to the bibliographical
                      data

        """
        release = StrictDict(str, releasedate=releasedate,
                             version=version, compiler=compiler,
                             compilerversion=compilerversion)
        self.releases.append((release, attached))

    def remove_release(self, version):
        """Remove a release from the story.

        Args:
            version: the version identifier of the release to remove

        """
        for release in self.releases:
            if release[0]["version"] == version:
                self.releases.remove(release)
                break

    def add_annotation(self, section_name, info_dict):
        """Add annotation to the story.

        Args:
            section_name: the name to give the annotation section
            info_dict: a nested dict containing the annotation data

        """
        self.annotation[section_name] = info_dict

    def remove_annotation(self, section_name):
        """Remove annotation.

        Args:
            section_name: the name of the annotation section to remove

        """
        del self.annotation[section_name]

    def _build_ifiction(self, ifiction_dom, truncate=False):
        """Helper function to build an IFiction file.

        Args:
            truncate: truncate text to 240 characters or 2400 characters for
                      the description (default: False)
        Returns:
            A tuple containing the DOM object and the story Node

        """
        story_node = ifiction.add_story(ifiction_dom)
        ifiction.add_identification(ifiction_dom, story_node, self.ifid_list,
                                    self.format, self.bafn)
        ifiction.add_bibliographic(ifiction_dom, story_node, truncate,
                                   **self.bibliographic)
        for resource in self.resources:
            ifiction.add_resource(ifiction_dom, story_node, resource[0], resource[1])
        if self.contacts["url"] != u"" or self.contacts["email"] != u"":
            ifiction.add_contacts(ifiction_dom, story_node,
                                  self.contacts["url"], self.contacts["email"])
        if self.cover.img_format:
            ifiction.add_cover(ifiction_dom, story_node, self.cover.img_format,
                               self.cover.height, self.cover.width,
                               self.cover.description)
        if len(self.format_info) > 0:
            ifiction.add_format_info(ifiction_dom, story_node, self.format,
                                     **self.format_info)
        for release in self.releases:
            rel_dict = release[0]
            ifiction.add_release(ifiction_dom, story_node,
                                 rel_dict["releasedate"],
                                 rel_dict["version"],
                                 rel_dict["compiler"],
                                 rel_dict["compilerversion"],
                                 release[1])
        if not self.colophon["generator"]:
            self.colophon["generator"] = u"pyifbabel"
            self.colophon["generatorversion"] = PYIFBABEL_VERSION
            self.colophon["originated"] = unicode(time.strftime("%x"))
        ifiction.add_colophon(ifiction_dom, story_node,
                              self.colophon["generator"],
                              self.colophon["originated"],
                              self.colophon["generatorversion"])
        for sect, info in self.annotation.items():
            ifiction.add_annotation(ifiction_dom, story_node, sect, info)
        return story_node

    def to_ifiction_story_node(self, ifiction_dom, truncate=False):
        """Create an IFiction story Node from the object.

        Args:
            truncate: truncate text to 240 characters or 2400 characters for
                      the description (default: False)
        Returns:
            A story Node

        """
        story_node = self._build_ifiction(ifiction_dom, truncate)
        return story_node

    def to_ifiction(self, indent="\t", truncate=False):
        """Create an IFiction XML document from the object.

        Args:
            indent: the character used to indent the XML (default: \\t)
            truncate: truncate text to 240 characters or 2400 characters for
                      the description (default: False)
        Returns:
            A DOM object

        """
        doc = ifiction.create_ifiction_dom()
        story_node = self._build_ifiction(doc, truncate)
        return doc.toprettyxml(indent=indent, encoding="UTF-8")

    def load_from_ifiction(self, story_node):
        """Load bibliographical data from an IFiction story Node.

        Args:
            story_node: an IFiction story Node

        """
        ident = ifiction.get_identification(story_node)
        for ifid in ident["ifid_list"]:
            if ifid not in self.ifid_list:
                self.ifid_list.append(ifid)
        self.format = ident["ifformat"]
        self.bafn = ident["bafn"]
        # In most cases, we don't want to copy the dict from ifiction
        # over to our local properties, since we'd prefer to keep the
        # StrictDict objects
        biblio = ifiction.get_bibliographic(story_node)
        for key, value in biblio.items():
            if value is None:
                value = ""
            self.bibliographic[key] = value
        self.resources = ifiction.get_resources(story_node)
        contacts = ifiction.get_contacts(story_node)
        for key, value in contacts.items():
            self.contacts[key] = value
        cover = ifiction.get_cover(story_node)
        self.cover.img_format = cover.get("format")
        self.cover.height = cover.get("height")
        self.cover.width = cover.get("width")
        self.cover.description = cover.get("description")
        self.format_info = ifiction.get_format_info(story_node)
        self.releases = ifiction.get_releases(story_node)
        colophon = ifiction.get_colophon(story_node)
        for key, val in colophon.items():
            self.colophon[key] = val
        self.annotation.update(ifiction.get_annotation(story_node))

    def load_from_story_file(self, story_file=None):
        """Load bibliographical data from a story file.

        If no story file is specified, the file name stored in self.story_file
        will be used.

        Args:
            story_file: the name of the story file to use (default: None)

        """
        if story_file is not None:
            self.story_file = story_file
        if self.story_file is None:
            return
        self.format = treatyofbabel.deduce_format(self.story_file)
        for ifid in treatyofbabel.get_ifids(self.story_file):
            if ifid not in self.ifid_list:
                self.ifid_list.append(ifid)
        meta = treatyofbabel.get_meta(self.story_file)
        if meta is not None:
            meta_dom = ifiction.get_ifiction_dom(meta)
            self.load_from_ifiction(meta_dom)
        cover = treatyofbabel.get_cover(self.story_file)
        if cover is not None:
            self.cover = cover

    def load_from_ifdb(self, ifid=None, tuid=None, fetch_cover=False):
        """Load bibliographical data from IFDB (http://ifdb.tads.org)

        Args:
            ifid: the IFID to search for (default: None; use the IFID stored
                  in self.ifid_list[0])
            tuid: the TUID to search for (default: None; try to use the TUID
                  stored in the object's annotation data)
            fetch_cover: fetch the cover art, if available (default: False)

        """
        if ifid is None and len(self.ifid_list) > 0:
                ifid = self.ifid_list[0]
        # try to get the tuid if it exists
        elif tuid is None and len(self.annotation) > 0:
            ifdb_annot = self.annotation.get("ifdb")
            if ifdb_annot is not None:
                tuid = ifdb_annot.get("tuid")
        # Access the IFDB public API
        if ifid is None and tuid is None:
            raise BabelError("No IFID or TUID set")
        if tuid is not None:
            url = ''.join(['http://ifdb.tads.org/viewgame?ifiction&id=',
                           tuid])
        else:
            url = ''.join(['http://ifdb.tads.org/viewgame?ifiction&ifid=',
                           ifid])
        ific = urlopen(url)
        ificstring = ific.read()
        try:
            ificdom = ifiction.get_ifiction_dom(ificstring)
        except IFictionError:
            raise IFictionError("Fetched content is not an IFiction file")
        ificstories = ifiction.get_all_stories(ificdom)
        if not ificstories or len(ificstories) == 0:
            raise IFictionError(
                "Fetched content does not contain a story element")
        ificstory = ificstories[0]
        ifiction.move_extra_to_annotation(ificdom, ificstory, ["ifdb"])
        self.load_from_ifiction(ificstory)
        if fetch_cover:
            self.load_cover_from_ifdb()
        return

    def load_cover_from_ifdb(self):
        ifdb_annot = self.annotation.get("ifdb")
        if ifdb_annot is None:
            return
        cover = ifdb_annot.get("coverart")
        if cover is None:
            return
        cover_url = cover.get("url")
        if cover_url is None:
            return
        cover_file = urlopen(cover_url)
        cover_data = cover_file.read()
        if cover_data is None:
            return
        fmt = deduce_img_format(cover_data)
        if fmt is None:
            return
        if fmt == "jpeg":
            width, height = get_jpeg_dim(cover_data)
        elif fmt == "png":
            width, height = get_png_dim(cover_data)
        else:
            width, height = get_gif_dim(cover_data)
        self.cover.data = cover_data
        self.cover.img_format = fmt
        self.cover.width = width
        self.cover.height = height
        self.cover.description = None
