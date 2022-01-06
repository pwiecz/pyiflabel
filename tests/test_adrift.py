# -*- coding: utf-8 -*-
#
#       test_adrift.py
#       
#       Copyright © 2011, 2012 Brandon Invergo <brandon@invergo.net>
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


import test_storyformat


class adriftTest(test_storyformat.StoryTest):
    def setUp(self):
        super(adriftTest, self).setUp('adrift')
    

if __name__ == "__main__":
    unittest.main()

    
