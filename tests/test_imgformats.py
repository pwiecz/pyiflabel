# -*- coding: utf-8 -*-
#
#       test_storyformat.py
#
#       Copyright © 2018 Brandon Invergo <brandon@invergo.net>
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
import glob
import os.path

from treatyofbabel.utils import _imgfuncs


class ImgTest(unittest.TestCase):
    def setUp(self):
        self.test_imgs = {"png": glob.glob("img/*.png"),
                          "jpeg": glob.glob("img/*.jpeg"),
                          "gif": glob.glob("img/*.gif")}

    def test_deduce_img_format(self):
        for img_fmt in self.test_imgs:
            for img in self.test_imgs[img_fmt]:
                with open(img, "rb") as h:
                    img_buf = h.read()
                self.assertEqual(_imgfuncs.deduce_img_format(img_buf),
                                 img_fmt)

    def test_get_jpeg_dim(self):
        jpgs = self.test_imgs["jpeg"]
        for img in jpgs:
            fname = os.path.basename(img).split(".")[0]
            dims = fname.split("-")[1]
            w, h = [int(x) for x in dims.split("x")]
            with open(img, "rb") as f:
                img_buf = f.read()
            test_w, test_h = _imgfuncs.get_jpeg_dim(img_buf)
            self.assertEqual(test_w, w)
            self.assertEqual(test_h, h)

    def test_get_png_dim(self):
        pngs = self.test_imgs["png"]
        for img in pngs:
            fname = os.path.basename(img).split(".")[0]
            dims = fname.split("-")[1]
            w, h = [int(x) for x in dims.split("x")]
            with open(img, "rb") as f:
                img_buf = f.read()
            test_w, test_h = _imgfuncs.get_png_dim(img_buf)
            self.assertEqual(test_w, w)
            self.assertEqual(test_h, h)

    def test_get_gif_dim(self):
        gifs = self.test_imgs["gif"]
        for img in gifs:
            fname = os.path.basename(img).split(".")[0]
            dims = fname.split("-")[1]
            w, h = [int(x) for x in dims.split("x")]
            with open(img, "rb") as f:
                img_buf = f.read()
            test_w, test_h = _imgfuncs.get_gif_dim(img_buf)
            self.assertEqual(test_w, w)
            self.assertEqual(test_h, h)
