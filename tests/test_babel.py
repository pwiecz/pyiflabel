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
import os.path

import treatyofbabel as babel
from treatyofbabel.babelerrors import BabelError


BABEL_FUNCS = [babel.deduce_format, babel.get_ifids, babel.get_meta, 
        babel.get_cover, babel.get_story, babel.verify_ifiction, 
        babel.ifiction_lint, babel.complete_ifiction, babel.make_blorb]


class BabelTest(unittest.TestCase):

    def test_emptyarg(self):
        with self.assertRaises(ValueError):
            for func in BABEL_FUNCS:
                func(None)
                func("")

    def test_badargtype(self):
        with self.assertRaises(TypeError):
            for func in BABEL_FUNCS:
                func(0)
                func([])
                func({})

    def test_badfilename(self):
        with self.assertRaises(IOError):
            for func in BABEL_FUNCS:
                func("i_do_not_exist.file")

    def test_notstoryfile(self):
        bad_story_file = os.path.join("resources", "notastory.bin")
        with self.assertRaises(BabelError):
            for func in BABEL_FUNCS:
                func(bad_story_file)

    def test_emptyfile(self):
        empty_story_file = os.path.join("resources", "emptyfile")
        with self.assertRaises(ValueError):
            for func in BABEL_FUNCS:
                func(empty_story_file)
