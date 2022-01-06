# -*- coding: utf-8 -*-
#
#       errors.py
#
#       Copyright © 2011, 2012, 2013, 2014, 2018 Brandon Invergo <brandon@invergo.net>
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


"""This module provides error classes to be raised by pyifbabel."""


class IFictionError(Exception):
    """Raised when an error occurs in reading or writing an IFiction file."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class BabelError(Exception):
    """Raised when an error occurs in determining information about a
    story file.

    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class BabelImgError(Exception):
    """Raised when an error occurs in determining information about an
    image file.

    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
