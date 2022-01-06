# -*- coding: utf-8 -*-
#
#       ifiction.py
#
#       Copyright © 2012, 2013, 2014, 2015, 2017, 2018 Brandon Invergo <brandon@invergo.net>
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


"""This module implements functions for reading and writing IFiction
files.  IFiction is an XML-based file format defined in the Treaty of
Babel.  Please note that the API is under heavy development and may
very well change following an impending switch in the underlying
Python XML parsing library.

"""


import xml.dom.minidom
from xml.parsers.expat import ExpatError

from babelerrors import IFictionError


BIBLIO_ATTR = ['title', 'author', 'language', 'headline',
               'firstpublished', 'genre', 'group', 'description',
               'series', 'seriesnumber', 'forgiveness']


IF_FORMATS = ["zcode", "glulx", "tads", "tads2", "tads3", "hugo", "alan",
              "adrift", "level9", "agt", "magscrolls", "advsys", "executable",
              "quest", "html", "twine"]


TOP_LEVELS = ["identification", "bibliographic", "resources", "contact",
              "cover art", "zcode", "tads2", "tads3", "glulx", "hugo",
              "adrift", "releases", "colophon", "annotation"]


def build_dict_from_node(xml_node):
    """Build a Python dict object from an XML node.

    Args:
        xml_node: an xml.dom Node
    Returns:
        A nested dict object containing the contents (and possible sub-
        contents) of the node.

    """
    node_dict = {}
    for child in xml_node.childNodes:
        name = child.nodeName.lower()
        if child.hasChildNodes():
            if name in node_dict:
                # For repeated entries, build up a list
                if isinstance(node_dict[name], list):
                    node_dict[name].append(build_dict_from_node(child))
                else:
                    node_dict[name] = [node_dict[name],
                                       build_dict_from_node(child)]
            else:
                node_dict[name] = build_dict_from_node(child)
        else:
            # This protects against weird XML formatting, like multiple text
            # child nodes at the same level
            if len(xml_node.childNodes) > 1:
                continue
            value = child.nodeValue
            if value is not None:
                value = value.strip()
            return value
    return node_dict


def build_node_from_dict(ifiction_dom, node_name, node_dict):
    """Build an xml.dom.minidom node from a nested dict object.

    Args:
        ifiction_dom: an xml.dom.minidom DOM object
        node_name: the name to be assigned to the node
        node_dict: the dict object from which to build the node
    Returns:
        The node object

    """
    node = ifiction_dom.createElement(node_name)
    for key, value in node_dict.items():
        key = key.lower()
        if value is None or value == "":
            continue
        child = None
        if isinstance(value, list):
            for val in value:
                tag = build_node_from_dict(ifiction_dom, key, val)
                node.appendChild(tag)
        elif isinstance(value, dict):
            if len(value.keys()) > 0:
                tag = build_node_from_dict(ifiction_dom, key, value)
            else:
                tag = ifiction_dom.createElement(key)
                child = ifiction_dom.createTextNode('')
            node.appendChild(tag)
        else:
            tag = ifiction_dom.createElement(key)
            child = ifiction_dom.createTextNode(value)
            node.appendChild(tag)
        if child is not None:
            tag.appendChild(child)
    return node


def is_ifiction(xml_dom_doc):
    """Test if an xml.dom Document contains IFiction data.

    Args:
        xml_dom_doc: the DOM object
    Returns:
        True if the object contains IFiction data, False otherwise

    """
    root = xml_dom_doc.documentElement
    xmlns = root.getAttribute("xmlns")
    if (xml_dom_doc.namespaceURI !=
        "http://babel.ifarchive.org/protocol/iFiction/" and
            xmlns != "http://babel.ifarchive.org/protocol/iFiction/"):
        return False
    root = xml_dom_doc.documentElement
    if root.nodeName != "ifindex":
        return False
    return True


def create_ifiction_dom():
    """Create a base DOM object for IFiction data.

    Returns:
        The xml.dom.minidom DOM object.

    """
    impl = xml.dom.minidom.getDOMImplementation()
    doc = impl.createDocument("http://babel.ifarchive.org/protocol/iFiction/",
                              "ifindex", None)
    root = doc.documentElement
    root.setAttribute("version", "1.0")
    root.setAttribute("xmlns", "http://babel.ifarchive.org/protocol/iFiction/")
    return doc


def munge_html(ifiction):
    """Munge various HTML tags to not be interpreted as XML data.

    For example, '<b>' will be replaced with '&lt;b&gt;'.

    Args:
        ifiction: a string containing the IFiction XML
    Returns:
        The ifiction string with HTML tags properly escaped.

    """
    html_tags = {'<b>': '&lt;b&gt;', '</b>': '&lt;&#47;b&gt;',
                 '<i>': '&lt;i&gt;', '</i>': '&lt;&#47;i&gt;',
                 '<p>': '&lt;p&gt;', '</p>': '&lt;&#47;p&gt;',
                 '<br/>': '&lt;br&#47;&gt;', '<br />': '&lt;br&#47;&gt;'}
    for tag, subs in html_tags.items():
        ifiction = ifiction.replace(tag, subs)
    return ifiction


def get_ifiction_dom(ifiction):
    """Construct an XML DOM object for an IFiction string.

    The text in the string will be properly munged and cleaned up as
    necessary.

    Args:
        ifiction: a string containing the IFiction XML
    Returns:
        An xml.dom.minidom DOM object

    """
    clean_ifiction = munge_html(ifiction)
    clean_ifiction = clean_ifiction.replace('\n', '')
    clean_ifiction = clean_ifiction.replace('\t', '')
    try:
        doc = xml.dom.minidom.parseString(clean_ifiction)
    except ExpatError:
        raise IFictionError("Malformed XML document")
    if not is_ifiction(doc):
        raise IFictionError("Document not IFiction")
    return doc


def add_comment(ifiction_dom, comment):
    """Add a comment to an IFiction DOM.

    Args:
        ifiction_dom: an xml.dom Document
        comment: the comment text

    """
    root = ifiction_dom.documentElement
    comment_node = ifiction_dom.createComment(comment)
    root.appendChild(comment_node)


def merge_story(ifiction_dom, story_node):
    """Merge a story Node into a DOM object.

    Args:
        ifiction_dom: an xml.dom Document
        story_node: an xml.dom.minidom node containing the story information

    """
    root = ifiction_dom.documentElement
    root.appendChild(story_node)


def add_story(ifiction_dom):
    """Create a new story Node for a DOM

    Args:
        ifiction_dom: an xml.dom Document
    Returns:
        The story Node

    """
    root = ifiction_dom.documentElement
    story_node = ifiction_dom.createElement("story")
    root.appendChild(story_node)
    ident = ifiction_dom.createElement("identification")
    story_node.appendChild(ident)
    biblio = ifiction_dom.createElement("bibliographic")
    story_node.appendChild(biblio)
    return story_node


def get_story(ifiction_dom, ifid):
    """Retrieve the node for a story with the given IFID from a DOM.

    Args:
        ifiction_dom: an xml.dom Document
        ifid: an IFID
    Returns:
        If a story with the given IFID is present in the IFiction data, its
        story Node will be returned, otherwise None

    """
    root = ifiction_dom.documentElement
    story_node_list = root.getElementsByTagName("story")
    for story_node in story_node_list:
        ident_list = story_node.getElementsByTagName("identification")
        if len(ident_list) > 0:
            ifid_node_list = story_node.getelementsByTagName("ifid")
            ifid_list = [node.firstChild.nodeValue.strip() for node in
                         ifid_node_list]
            if ifid in ifid_list:
                return story_node
    return None


def get_all_stories(ifiction_dom):
    """Retrieve all story Nodes from a DOM.

    Args:
        ifiction_dom: an xml.dom Document
    Returns:
        A NodeList containing all of the story Nodes

    """
    root = ifiction_dom.documentElement
    return root.getElementsByTagName("story")


def add_identification(ifiction_dom, story_node, ifid_list, ifformat,
                       bafn=None):
    """Add identification information to a story Node.

    Args:
        ifiction_dom: an xml.dom Document
        story_node: a story Node
        ifid_list: a list of IFIDs
        ifformat: a sttring describing the format of the story file
        bafn: a BAFN number for the file (default: None)
    Raises:
        IFictionError if any of the elements do not conform to the IFiction
        standard

    """
    ident = story_node.getElementsByTagName("identification")[0]
    invalid_ifids = 0
    if len(ifid_list) == 0:
        raise IFictionError("identification: IFID required")
    for ifid in ifid_list:
        if ifid is None or ifid == "":
            invalid_ifids += 1
        ifid_tag = ifiction_dom.createElement("ifid")
        ident.appendChild(ifid_tag)
        ifid_text = ifiction_dom.createTextNode(ifid)
        ifid_tag.appendChild(ifid_text)
    if invalid_ifids == len(ifid_list):
        raise IFictionError("identification: IFID required")
    if ifformat is None or ifformat == "":
        raise IFictionError("identification: format required")
    if ifformat not in IF_FORMATS:
        raise IFictionError("identification: invalid format")
    format_tag = ifiction_dom.createElement("format")
    ident.appendChild(format_tag)
    format_text = ifiction_dom.createTextNode(ifformat)
    format_tag.appendChild(format_text)
    if bafn is not None and bafn != "":
        try:
            if int(bafn) <= 0:
                raise IFictionError(
                    "identification: bafn must be a positive integer")
        except:
            raise IFictionError(
                "identification: bafn must be a positive integer")
        bafn_tag = ifiction_dom.createElement("bafn")
        ident.appendChild(bafn_tag)
        bafn_text = ifiction_dom.createTextNode(bafn)
        bafn_tag.appendChild(bafn_text)


def get_identification(story_node):
    """Return a nested dict object containing story identification data.

    Args:
        story_node: a story Node
    Returns:
        A dict object with node names as keys and node text as values

    """
    info = {"ifid_list": None, "ifformat": None, "bafn": None}
    ident = story_node.getElementsByTagName("identification")[0]
    ifid_tag_list = ident.getElementsByTagName("ifid")
    ifid_list = []
    for ifid_tag in ifid_tag_list:
        ifid_list.append(ifid_tag.firstChild.nodeValue.strip())
    info["ifid_list"] = ifid_list
    format_tag_list = ident.getElementsByTagName("format")
    # There should always be a format tag but even if the iFiction is malformed
    # we should still try to parse it. Maybe issue a warning here.
    if len(format_tag_list) > 0:
        format_tag = format_tag_list[0]
        info["ifformat"] = format_tag.firstChild.nodeValue.strip()
    bafn_tag_list = ident.getElementsByTagName("bafn")
    if len(bafn_tag_list) > 0:
        bafn_tag = bafn_tag_list[0]
        info["bafn"] = bafn_tag.firstChild.nodeValue.strip()
    return info


def check_identification(story_node):
    pass


def lint_identification(ifiction_dom):
    pass


def add_bibliographic(ifiction_dom, story_node, truncate=False, **kwargs):
    """Add bibliographic information to a story Node.

    Args:
        ifiction_dom: an xml.dom Document
        story_node: a story Node
        truncate: truncate text data to 240 characters (2400 characters for
                  the description)
    Additional keyword args:
        title: the story's title (required)
        author: the story' author (required)
        language: the (human) language used by the story
        headline: the story's headline/subtitle
        firstpublished: the year/date when the story was first published
        genre: the story's genre
        group: the group to which the story belongs (e.g. publisher or comp)
        description: a long description of the story
        series: the series to which the story belongs
        seriesnumber: the story's position in the series
        forgiveness: the story's difficulty on zarf's forgiveness scale
    Raises:
        IFictionError if any of the elements do not conform to the IFiction
        standard

    """
    biblio = story_node.getElementsByTagName("bibliographic")[0]
    if kwargs.get("author") is None or kwargs["author"] == "":
        raise IFictionError("bibliographic: author required")
    if kwargs.get("title") is None or kwargs["title"] == "":
        raise IFictionError("bibliographic: title required")
    for key, value in kwargs.items():
        if key not in BIBLIO_ATTR:
            raise IFictionError("bibliographic: invalid tag "+key)
        if value == "" or value is None:
            continue
        if truncate:
            if key == "description" and len(value) > 2400:
                value = value[:2401]
            elif len(value) > 240:
                value = value[:241]
        tag = ifiction_dom.createElement(key)
        biblio.appendChild(tag)
        tag_text = ifiction_dom.createTextNode(value)
        tag.appendChild(tag_text)


def get_bibliographic(story_node):
    """Return a nested dict object containing story bibliographic data.

    Args:
        story_node: a story Node
    Returns:
        A dict object with node names as keys and node text as values

    """
    info = dict(zip(BIBLIO_ATTR, [None for x in range(len(BIBLIO_ATTR))]))
    biblio = story_node.getElementsByTagName("bibliographic")[0]
    for node in biblio.childNodes:
        if node.nodeName not in info:
            continue
        if node.firstChild is not None:
            info[node.nodeName] = node.firstChild.nodeValue.strip()
        else:
            info[node.nodeName] = None
    return info


def check_bibliographic(ifiction_dom):
    pass


def lint_bibliographic(ifiction_dom):
    pass


def add_resource(ifiction_dom, story_node, leafname, description):
    """Add resource information to a story Node.

    Args:
        ifiction_dom: an xml.dom Document
        story_node: a story Node
        leafname: the resource file name
        description: a description of the resource
    Raises:
        IFictionError if any of the elements do not conform to the IFiction
        standard

    """
    res_list = story_node.getElementsByTagName("resources")
    if len(res_list) == 0:
        res = ifiction_dom.createElement("resources")
        story_node.appendChild(res)
    else:
        res = res_list[0]
    if leafname == "" or leafname is None:
        raise IFictionError("resource: file name required")
    if description == "" or description is None:
        raise IFictionError("resource: description required")
    aux = ifiction_dom.createElement("auxiliary")
    res.appendChild(aux)
    leafname_tag = ifiction_dom.createElement("leafname")
    aux.appendChild(leafname_tag)
    leafname_text = ifiction_dom.createTextNode(leafname)
    leafname_tag.appendChild(leafname_text)
    descrip_tag = ifiction_dom.createElement("description")
    aux.appendChild(descrip_tag)
    descrip_text = ifiction_dom.createTextNode(description)
    descrip_tag.appendChild(descrip_text)


def get_resources(story_node):
    """Return a nested dict object containing story resource data.

    Args:
        story_node: a story Node
    Returns:
        A dict object with node names as keys and node text as values

    """
    res_list = []
    resources = story_node.getElementsByTagName("resources")
    if len(resources) > 0:
        aux_list = resources.getElementsByTagName("auxiliary")
        for aux in aux_list:
            resource = {"leafname": None, "description": None}
            leaf_list = aux.getElementsByTagName("leafname")
            if len(leaf_list) > 0:
                leafname = leaf_list[0].firstChild.nodeValue.strip()
                resource["leafname"] = leafname
            desc_list = aux.getElementsByTagName("description")
            if len(desc_list) > 0:
                desc = desc_list[0].firstChild.nodeValue.strip()
                resource["description"] = desc
    return res_list


def check_resource(ifiction_dom):
    pass


def lint_resource(ifiction_dom):
    pass


def add_contact(ifiction_dom, story_node, url=None, email=None):
    """Add contact information to a story Node.

    Args:
        ifiction_dom: an xml.dom Document
        story_node: a story Node
        url: a URL for the author/story (default: None)
        email: an email address for the author (default: None)
    Raises:
        IFictionError if any of the elements do not conform to the IFiction
        standard

    """
    if (url is None or url == "") and (email is None or email == ""):
        raise IFictionError("contact: either a URL or Email address required")
    if len(story_node.getElementsByTagName("contact")) != 0:
        raise IFictionError("contact: contact section already exists")
    cont = ifiction_dom.createElement("contact")
    story_node.appendChild(cont)
    if url is not None and url != "":
        url_tag = ifiction_dom.createElement("url")
        cont.appendChild(url_tag)
        url_text = ifiction_dom.createTextNode(url)
        url_tag.appendChild(url_text)
    if email is not None and email != "":
        email_tag = ifiction_dom.createElement("email")
        cont.appendChild(email_tag)
        email_text = ifiction_dom.createTextNode(email)
        email_tag.appendChild(email_text)


def get_contact(story_node):
    """Return a nested dict object containing story contact data.

    Args:
        story_node: a story Node
    Returns:
        A dict object with node names as keys and node text as values

    """
    contact = {"url": None, "email": None}
    contact_nodes = story_node.getElementsByTagName("contact")
    if len(contact_nodes) > 0:
        url_nodes = contact_nodes[0].getElementsByTagName("url")
        if len(url_nodes) > 0:
            contact["url"] = url_nodes[0].firstChild.nodeValue.strip()
        email_nodes = contact_nodes[0].getElementsByTagName("email")
        if len(email_nodes) > 0:
            contact["email"] = email_nodes[0].firstChild.nodeValue.strip()
    return contact


def check_contact(ifiction_dom):
    pass


def lint_contact(ifiction_dom):
    pass


def add_cover(ifiction_dom, story_node, img_format, height, width,
              description):
    """Add cover art information to a story Node.

    Args:
        ifiction_dom: an xml.dom Document
        story_node: a story Node
        img_format: the file format of the image ('jpg', 'png', or 'gif')
        height: the height in pixels of the image
        width: the width in pixels of the image
        description: a description of the contents of the image
    Raises:
        IFictionError if any of the elements do not conform to the IFiction
        standard
    Note:
        Support for GIF images is a pyifbabel extension to the original Treaty 
        of Babel

    """
    if img_format is None or img_format == "":
        raise IFictionError("cover: image format required")
    if img_format not in ["jpg", "png", "gif"]:
        raise IFictionError("cover: invalid image format")
    if height is None or height == "":
        raise IFictionError("cover: image height required")
    try:
        if int(height) <= 0:
            raise IFictionError("cover: height must be a positive integer")
    except:
        raise IFictionError("cover: height must be a positive integer")
    if width is None or width == "":
        raise IFictionError("cover: image width required")
    try:
        if int(width) <= 0:
            raise IFictionError("cover: width must be a positive integer")
    except:
        raise IFictionError("cover: width must be a positive integer")
    if len(story_node.getElementsByTagName("cover")) != 0:
        raise IFictionError("cover: cover section already exists")
    cov = ifiction_dom.createElement("cover")
    story_node.appendChild(cov)
    format_tag = ifiction_dom.createElement("format")
    cov.appendChild(format_tag)
    format_text = ifiction_dom.createTextNode(img_format)
    format_tag.appendChild(format_text)
    height_tag = ifiction_dom.createElement("height")
    cov.appendChild(height_tag)
    height_text = ifiction_dom.createTextNode(str(height))
    height_tag.appendChild(height_text)
    width_tag = ifiction_dom.createElement("width")
    cov.appendChild(width_tag)
    width_text = ifiction_dom.createTextNode(str(width))
    width_tag.appendChild(width_text)
    if description is not None:
        descr_tag = ifiction_dom.createElement("description")
        cov.appendChild(descr_tag)
        descr_text = ifiction_dom.createTextNode(description)
        descr_tag.appendChild(descr_text)


def get_cover(story_node):
    """Return a nested dict object containing story cover art data.

    Args:
        story_node: a story Node
    Returns:
        A dict object with node names as keys and node text as values

    """
    cover = {"format": None, "height": None, "width": None,
             "description": None}
    cover_nodes = story_node.getElementsByTagName("cover")
    if len(cover_nodes) > 0:
        cover_node = cover_nodes[0]
        format_nodes = cover_node.getElementsByTagName("format")
        if len(format_nodes) > 0:
            cover["format"] = format_nodes[0].firstChild.nodeValue.strip()
        height_nodes = cover_node.getElementsByTagName("height")
        if len(height_nodes) > 0:
            cover["height"] = height_nodes[0].firstChild.nodeValue.strip()
        width_nodes = cover_node.getElementsByTagName("width")
        if len(width_nodes) > 0:
            cover["width"] = width_nodes[0].firstChild.nodeValue.strip()
        descr_nodes = cover_node.getElementsByTagName("description")
        if len(descr_nodes) > 0:
            cover["description"] = descr_nodes[0].firstChild.nodeValue.strip()
    return cover


def check_cover(ifiction_dom):
    pass


def lint_cover(ifiction_dom):
    pass


def add_format_info(ifiction_dom, story_node, ifformat, **kwargs):
    """Add format-specific information to a story Node.

    Args:
        ifiction_dom: an xml.dom Document
        story_node: a story Node
        ifformat: the file format of the story
    Additional keyword args:
        Any keyword will be accepted and converted into a child node (e.g.
        'version=8' will be used as '<version>8</version>'
    Raises:
        IFictionError if any of the elements do not conform to the IFiction
        standard

    """
    if ifformat not in IF_FORMATS:
        raise IFictionError("format-specific: invalid format")
    ident = story_node.getElementsByTagName("identification")[0]
    story_format_node = ident.getElementsByTagName("format")[0]
    story_format = story_format_node.firstChild.nodeValue.strip()
    if story_format in ["tads2", "tads3"]:
        story_format = "tads"
    if ifformat != story_format:
        raise IFictionError(
            "format-specific: format does not match story format")
    if len(story_node.getElementsByTagName(ifformat)) != 0:
        raise IFictionError(
            "format-specific: format-specific section already exists")
    format_tag = build_node_from_dict(ifiction_dom, ifformat, kwargs)
    story_node.appendChild(format_tag)


def get_format_info(story_node):
    """Return a nested dict object containing story format-specific data.

    Args:
        story_node: a story Node
    Returns:
        A dict object with node names as keys and node text as values

    """
    info = {}
    ident = story_node.getElementsByTagName("identification")[0]
    format_nodes = ident.getElementsByTagName("format")
    ifformat = None
    if len(format_nodes) > 0:
        format_node = format_nodes[0]
        ifformat = format_node.firstChild.nodeValue.strip()
    format_info_nodes = story_node.getElementsByTagName(ifformat)
    if len(format_info_nodes) > 0:
        info = build_dict_from_node(format_info_nodes[0])
    return info


def check_format_info(ifiction_dom):
    pass


def lint_format_info(ifiction_dom):
    pass


def add_release(ifiction_dom, story_node, releasedate, version=None,
                compiler=None, compilerversion=None, attached=False):
    """Add release information to a story Node.

    Args:
        ifiction_dom: an xml.dom Document
        story_node: a story Node
        releasedate: the story's release date
        version: the story's version identifier (default: None)
        compiler: the compiler used to create the story (default: None)
        compilerversion: the compiler's version identifier (default: None)
        attached: True if the story file is attached to the IFiction document
                  (default: False)
    Raises:
        IFictionError if any of the elements do not conform to the IFiction
        standard

    """
    if releasedate is None or releasedate == "":
        raise IFictionError("releases: release date is required")
    if ((compiler is None or compiler == "") and
            (compilerversion is not None and compilerversion != "")):
        raise IFictionError(
            "releases: compiler version requires compiler info")
    rel_list = story_node.getElementsByTagName("releases")
    if len(rel_list) == 0:
        releases = ifiction_dom.createElement("releases")
        story_node.appendChild(releases)
    else:
        releases = rel_list[0]
    if attached is True:
        if len(releases.getElementsByTagName("attached")) != 0:
            raise IFictionError("releases: attached release already exists")
        parent_tag = ifiction_dom.createElement("attached")
        releases.appendChild(parent_tag)
    else:
        hist_list = releases.getElementsByTagName("history")
        if len(hist_list) == 0:
            parent_tag = ifiction_dom.createElement("history")
            releases.appendChild(parent_tag)
        else:
            parent_tag = hist_list[0]
    rel_tag = ifiction_dom.createElement("release")
    parent_tag.appendChild(rel_tag)
    date_tag = ifiction_dom.createElement("releasedate")
    rel_tag.appendChild(date_tag)
    date_text = ifiction_dom.createTextNode(releasedate)
    date_tag.appendChild(date_text)
    if version is not None and version != "":
        vers_tag = ifiction_dom.createElement("version")
        rel_tag.appendChild(vers_tag)
        vers_text = ifiction_dom.createTextNode(version)
        vers_tag.appendChild(vers_text)
    if compiler is not None and compiler != "":
        comp_tag = ifiction_dom.createElement("compiler")
        rel_tag.appendChild(comp_tag)
        comp_text = ifiction_dom.createTextNode(compiler)
        comp_tag.appendChild(comp_text)
    if compilerversion is not None and compilerversion != "":
        compvers_tag = ifiction_dom.createElement("compilerversion")
        rel_tag.appendChild(compvers_tag)
        compvers_text = ifiction_dom.createTextNode(compilerversion)
        compvers_tag.appendChild(compvers_text)


def get_releases(story_node):
    """Return a nested dict object containing story release data.

    Args:
        story_node: a story Node
    Returns:
        A dict object with node names as keys and node text as values

    """
    releases = []
    releases_nodes = story_node.getElementsByTagName("releases")
    if len(releases_nodes) == 0:
        return releases
    releases_node = releases_nodes[0]
    attached_nodes = releases_node.getElementsByTagName("attached")
    if len(attached_nodes) > 0:
        attached_node = attached_nodes[0]
        release_nodes = attached_node.getElementsByTagName("release")
        if len(release_nodes) > 0:
            release_node = release_nodes[0]
            release = ({"releasedate": None, "version": None,
                        "compiler": None, "compilerversion": None}, True)
            for node in release_node.childNodes:
                if node.hasChildNodes():
                    child = node.firstChild
                    release[0][node.nodeName] = child.nodeValue.strip()
            releases.append(release)
    hist_nodes = releases_node.getElementsByTagName("history")
    if len(hist_nodes) > 0:
        hist_node = hist_nodes[0]
        release_nodes = hist_node.getElementsByTagName("release")
        for release_node in release_nodes:
            release = ({"releasedate": None, "version": None,
                        "compiler": None, "compilerversion": None}, False)
            for node in release_node.childNodes:
                release[0][node.nodeName] = node.firstChild.nodeValue
            releases.append(release)
    return releases


def check_releases(ifiction_dom):
    pass


def lint_releases(ifiction_dom):
    pass


def add_colophon(ifiction_dom, story_node, generator, originated,
                 generatorversion=None):
    """Add colophon information to a story Node.

    Args:
        ifiction_dom: an xml.dom Document
        story_node: a story Node
        generator: the name of the tool generating the IFiction record
        originated: the date the bibliographic data was last approved by the
                    author of the work
        generatorversion: the generator's version identifier (default: None)
    Raises:
        IFictionError if any of the elements do not conform to the IFiction
        standard

    """
    if generator is None or generator == "":
        raise IFictionError("colophon: generator is required")
    if originated is None or originated == "":
        raise IFictionError("colophon: originated is required")
    if len(story_node.getElementsByTagName("colophon")) != 0:
        raise IFictionError("colophon: colophon section already exists")
    colophon = ifiction_dom.createElement("colophon")
    story_node.appendChild(colophon)
    gen_tag = ifiction_dom.createElement("generator")
    colophon.appendChild(gen_tag)
    gen_text = ifiction_dom.createTextNode(generator)
    gen_tag.appendChild(gen_text)
    if generatorversion is not None and generatorversion != "":
        genvers_tag = ifiction_dom.createElement("generatorversion")
        colophon.appendChild(genvers_tag)
        genvers_text = ifiction_dom.createTextNode(generatorversion)
        genvers_tag.appendChild(genvers_text)
    orig_tag = ifiction_dom.createElement("originated")
    colophon.appendChild(orig_tag)
    orig_text = ifiction_dom.createTextNode(originated)
    orig_tag.appendChild(orig_text)


def get_colophon(story_node):
    """Return a nested dict object containing story colophon data.

    Args:
        story_node: a story Node
    Returns:
        A dict object with node names as keys and node text as values

    """
    colophon = {"generator": None, "generatorversion": None,
                "originated": None}
    colophon_nodes = story_node.getElementsByTagName("colophon")
    if len(colophon_nodes) > 0:
        colophon_node = colophon_nodes[0]
        for node in colophon_node.childNodes:
            if node.nodeName not in colophon:
                continue
            colophon[node.nodeName] = node.firstChild.nodeValue.strip()
    return colophon


def check_colophon(ifiction_dom):
    pass


def lint_colophon(ifiction_dom):
    pass


def add_annotation(ifiction_dom, story_node, section_name, info_dict):
    """Add annotation to a story Node.

    Args:
        ifiction_dom: an xml.dom Document
        story_node: a story Node
        section_name: the name to give the annotation child node
        info_dict: a nested dict object containing the annotation data
    Raises:
        IFictionError if any of the elements do not conform to the IFiction
        standard

    """
    if section_name is None or section_name == "":
        raise IFictionError("annotation: section name is required")
    if len(info_dict) == 0:
        raise IFictionError("annotation: no additional tags passed")
    annot_list = story_node.getElementsByTagName("annotation")
    if len(annot_list) == 0:
        annot = ifiction_dom.createElement("annotation")
        story_node.appendChild(annot)
    else:
        annot = annot_list[0]
        if len(annot.getElementsByTagName(section_name)) != 0:
            raise IFictionError(
                "annotation: {0} section already exists".format(section_name))
    sect_tag = build_node_from_dict(ifiction_dom, section_name, info_dict)
    annot.appendChild(sect_tag)


def get_annotation(story_node):
    """Return a nested dict object containing story annotation data.

    Args:
        story_node: a story Node
    Returns:
        A dict object with node names as keys and node text as values

    """
    annotations = {}
    annot_nodes = story_node.getElementsByTagName("annotation")
    if len(annot_nodes) > 0:
        sect_list = annot_nodes[0].childNodes
        for sect_node in sect_list:
            if sect_node.nodeType != sect_node.TEXT_NODE:
                sect_name = sect_node.nodeName
                sect_info = build_dict_from_node(sect_node)
                annotations[sect_name] = sect_info
    return annotations


def move_extra_to_annotation(ifiction_dom, story_node, extra_nodes=None):
    """Move any non-canonical, extra nodes to the annotation section.

    Some IFiction generators create top-level nodes that are not
    specified in the Treaty of Babel standard.  These should probably
    be moved under the <annotation> tag.  This function does that.

    Args:
        ifiction_dom: an xml.dom Document
        story_node: a story Node
        extra_nodes: a list names of nodes to be moved

    """
    if isinstance(extra_nodes, str):
        extra_nodes_list = [extra_nodes]
    else:
        extra_nodes_list = extra_nodes
    nodes = []
    if extra_nodes is None:
        for node in story_node.childNodes():
            if node.nodeName not in TOP_LEVELS:
                nodes.append(node)
    else:
        for node_name in extra_nodes_list:
            node_list = story_node.getElementsByTagName(node_name)
            if len(node_list) > 0:
                node = node_list[0]
                nodes.append(node)
    annot_list = story_node.getElementsByTagName("annotation")
    if len(annot_list) == 0:
        annot = ifiction_dom.createElement("annotation")
        story_node.appendChild(annot)
    else:
        annot = annot_list[0]
    for node in nodes:
        node_copy = node.cloneNode(True)
        story_node.removeChild(node)
        annot.appendChild(node_copy)


def check_annotation(ifiction_dom):
    pass


def lint_annotation(ifiction_dom):
    pass


def check_ifiction(ifiction):
    pass


def lint_ifiction(ifiction):
    pass
