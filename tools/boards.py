# !/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the uPiot project, https://github.com/gepd/upiot/
#
# MIT License
#
# Copyright (c) 2017 GEPD
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from os import path
from glob import glob
from ..tools import paths


def boards_list():
    """List of boards

    Get a list of boards based in the json files located
    in Packages/uPIOT/boards

    Returns:
        [list] -- list with board names
    """
    boards_path = paths.boards_folder()
    boards_path = path.join(boards_path, '*')

    board_list = []
    for board in glob(boards_path):
        board_list.append(get_filename(board))
    return board_list


def get_filename(filepath, ext=False):
    """Get file name

    Get the file name from a given path

    Arguments:
        path {str} -- path with the file.ext

    Keyword Arguments:
        ext {bool} -- if false remove the extension (default: {False})

    Returns:
        str -- filename or filename.ext
    """
    filename = path.basename(filepath)

    if(not ext):
        filename = filename.split(".")[0]
    return filename
