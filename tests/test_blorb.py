# -*- coding: utf-8 -*-
#
#       test_blorb.py
#       
#       Copyright © 2011, 2014 Brandon Invergo <brandon@invergo.net>
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


import test_storyformat


class blorbTest(test_storyformat.StoryTest):
    def setUp(self):
        super(blorbTest, self).setUp('blorb')


if __name__ == "__main__":
    unittest.main()
