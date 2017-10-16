# !/usr/bin/env python
# -*- coding: utf-8 -*-
from os import path
from glob import glob
from ..tools import paths


def get_boards_list():
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
