# -*- coding: utf-8 -*-
#
#       test_tads.py
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


class questTest(test_storyformat.StoryTest):
    def setUp(self):
        super(questTest, self).setUp('quest')
        self.babel_override = {
            "quest/Dragon.quest": {
                "format": 'quest',
                "ifids": ["0fd8a779-cf0e-4d87-b243-237cf4a1fce4"],
                "bibliographic": {
                    "author": "Craig Dutton (c) 2012",
                    "title": "Dragon",
                    "genre": "Fantasy",
                    "description": "You are on a mission to find the Dragon who \
                        is residing somewhere hidden in this kingdom. The hoard\
                        of treasure it protects would bring prosperity to \
                        anyone brave enough to confront and defeat this creature."
                    }
                },
            "quest/Escape from Byron Bay.quest": {
                "format": "quest",
                "ifids": ["5ed0a10a-a86f-4adb-a926-a168cc013e78"],
                "bibliographic": {
                    "author": "Allen Heard",
                    "title": "Escape from Byron Bay",
                    "genre": "Puzzle",
                    "description": "A bustling tourist attraction is turned on \
                        its head when a medical company makes an error. \
                        Bryneli-Med staff flee leaving you to face more than \
                        the music. Can you solve the puzzles and escape from \
                        Byron Bay."
                    }
                },
            "quest/Fun tiemz.quest": {
                "format": "quest",
                "ifids": ["05df260f-2035-47f1-87c5-45f41ce0f657"],
                "bibliographic": {
                    "author": "Spork",
                    "title": "Fun Tiemz",
                    "genre": "Romance",
                    "description": "What even is this, I don't know. |D Enjoy"
                    }
                },
            "quest/Settler of the Wastes.quest": {
                "format": "quest",
                "ifids": ["4bb3bad6-71a5-4bd4-92b3-8988352e7005"],
                "bibliographic": {
                    "author": "Joshua Aguire- Graphics by Jelly Bear",
                    "title": "Settler of the Wastes",
                    "genre": "RPG",
                    "description": None
                    }
                }
            }

if __name__ == "__main__":
    unittest.main()
