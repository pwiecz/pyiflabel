# -*- coding: utf-8 -*-
#
#       test_twine.py
#
#       Copyright © 2018 Brandon Invergo <brandon@invergo.net>
#
#       This file is part of pyIFBable.
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


import test_storyformat


class TwineTest(test_storyformat.StoryTest):
    def setUp(self):
        super(TwineTest, self).setUp('twine')
        self.babel_override = {
            "twine/abbess-otilias.html": {
                "format": 'twine',
                "ifids": ["94D68358-2F2B-4E24-825B-5558DD4EEC9E"]
            },
            "twine/Adventures_with_Fido.html": {
                "format": 'twine',
                "ifids": ["859229BD-CE3A-49F5-ABA3-D0C3FA572595"]
            },
            "twine/Animalia.html": {
                "format": 'twine',
                "ifids": ["AEA8DA1E-46F5-4C0E-BB7F-5E8ECC3C95E6"]
            }}


if __name__ == "__main__":
    unittest.main()
