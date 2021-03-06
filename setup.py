#!/usr/bin/env python
# setup.py.in --- 

# Copyright (C) 2014 Brandon Invergo <brandon@invergo.net>

# Author: Brandon Invergo <brandon@invergo.net>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from distutils.core import setup
import platform
import os.path

if platform.system() == 'Linux':
    doc_dir = '/usr/local/share/doc/pyifbabel'
else:
    try:
        from win32com.shell import shellcon, shell
        homedir = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0)
        appdir = 'pyifbabel'
        doc_dir = os.path.join(homedir, appdir)
    except:
        pass

long_desc = """pyifbabel is a libary and command-line tool for extracting
metadata information from interactive fiction (a.k.a. "text adventure") game
files."""

setup(name='pyifbabel',
      version='0.4',
      description='A pure-Python implementation of the Treaty of Babel',
      long_description=long_desc,
      author='Brandon Invergo',
      author_email='brandon@invergo.net',
      url='http://pyifbabel.invergo.net/',
      packages=['treatyofbabel', 'treatyofbabel.formats',
                'treatyofbabel.utils', 'treatyofbabel.wrappers'],
      scripts=['pyifbabel'],
      data_files=[(doc_dir, ['COPYING', 'README', 'USAGE'])],
      license='GPLv3',
      platforms=['Any'],
      classifiers=[
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Development Status :: 4 - Beta',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.5',
          'Operating System :: OS Independent',
          'Intended Audience :: Developers',
          'Topic :: Games/Entertainment'],)
