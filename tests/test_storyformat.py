# -*- coding: utf-8 -*-
#
#       test_storyformat.py
#       
#       Copyright © 2011, 2012, 2013, 2014 Brandon Invergo <brandon@invergo.net>
#       
#       This file is part of pyIFBabel.
#
#       pyIFBabel is free software: you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation, either version 3 of the License, or
#       (at your option) any later version.
#
#       pyIFBabel is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with pyIFBabel.  If not, see <http://www.gnu.org/licenses/>.


import unittest
import subprocess
import os

import treatyofbabel as babel
from treatyofbabel import ifiction


def format_error(story_path, item, incorrect, correct):
    return 'Wrong {1}: {0}\n{2} != {3}'.format(story_path, item, incorrect,
                                               correct)

class StoryTest(unittest.TestCase):
    def setUp(self, story_file_dir):
        self.test_stories = []
        self.babel_override = {}
        for story in os.listdir(story_file_dir):
            story_path = os.path.join(story_file_dir, story)
            self.test_stories.append(story_path)

    def test_format(self):
        for story_path in self.test_stories:
            story_override = self.babel_override.get(story_path)
            if story_override is not None:
                CBabel_format = story_override.get("format")
            else:
                babel_format_res = subprocess.check_output(['babel',
                                                          '-format',
                                                          story_path])
                CBabel_format = babel_format_res.split(':')[1].strip()
            ifformat = babel.deduce_format(story_path)
            self.assertEqual(ifformat, CBabel_format,
                             format_error(story_path, 'format',
                                          ifformat, CBabel_format))

    def test_ifid(self):
        for story_path in self.test_stories:
            story_override = self.babel_override.get(story_path)
            if story_override is not None:
                CBabel_ifids = story_override.get("ifids")
            else:
                babel_ifid_res = subprocess.check_output(['babel',
                                                          '-ifid',
                                                          story_path])
                CBabel_ifid_lines = babel_ifid_res.strip().split('\n')
                CBabel_ifids = [line.split(':')[1].strip() for line in CBabel_ifid_lines]
            ifids = babel.get_ifids(story_path)
            self.assertEqual(ifids, CBabel_ifids,
                             format_error(story_path, 'IFID',
                                          ifids, CBabel_ifids))

    def test_meta(self):
        for story_path in self.test_stories:
            story_override = self.babel_override.get(story_path)
            if story_override is not None:
                babel_meta_dom = ifiction.create_ifiction_dom()
                story = ifiction.add_story(babel_meta_dom)
                ifiction.add_identification(babel_meta_dom, story, 
                        story_override.get("ifids"), 
                        story_override.get("format"))
                biblio = story_override.get("bibliographic")
                if biblio is not None:
                    ifiction.add_bibliographic(babel_meta_dom, story, False,
                            **story_override.get("bibliographic"))
            else:
                babel_meta_res = subprocess.check_output(['babel',
                                                          '-meta',
                                                          story_path])
                try:
                    babel_meta_dom = xml.dom.minidom.parseString(babel_meta_res)
                except:
                    babel_meta_dom = None
            meta = babel.get_meta(story_path)
            try:
                meta_dom = xml.dom.minidom.parseString(meta)
            except:
                meta_dom = None
            if meta_dom is not None and babel_meta_dom is not None:
                self.assertEqual(meta_dom, babel_meta_dom,
                                 format_error(story_path, 'meta',
                                     meta_dom.toprettyxml(encoding="UTF-8", 
                                        indent="  "), 
                                     babel_meta_dom.toprettyxml(encoding="UTF-8",
                                        indent="  ")))

    def test_cover(self):
        for story_path in self.test_stories:
            babel_info = subprocess.check_output(['babel',
                                                  '-identify',
                                                  story_path]).strip()
            babel_info_str = babel_info.rsplit('\n', 1)[1]
            babel_info_cover = babel_info_str.rsplit(',', 1)[1].strip()
            cover = babel.get_cover(story_path)
            if cover is None:
                cover_str = "no cover"
            else:
                if cover.img_format == 'jpg':
                    cover.img_format = 'jpeg'
                cover_str = "cover {0}x{1} {2}".format(cover.width, cover.height, 
                        cover.img_format) 
            self.assertEqual(cover_str, babel_info_cover,
                            format_error(story_path, 'cover',
                                         cover_str, babel_info_cover))


if __name__ == "__main__":
    unittest.main()

    
