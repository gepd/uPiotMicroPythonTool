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

from inspect import currentframe, getfile
from os import path, makedirs

#
# Plugin Paths
#

current_file = path.abspath(getfile(currentframe()))


def plugin_folder():
    """
    Get absolute path of the plugin Packages/uPIOT
    """
    plugin_path = path.dirname(path.dirname(current_file))
    return plugin_path


def plugin_name():
    """
    Get the plugin folder name
    """
    plugin_path = plugin_folder()
    return path.basename(plugin_path)


def esptool_file():
    """
    Get the path of the esptool.py file
    """
    plugin_path = plugin_folder()
    tools_path = path.join(plugin_path, 'tools', 'esptool.py')
    return tools_path


def upiot_user_folder():
    """
    ~/.upiot/
    """
    user_path = path.expanduser('~')
    upiot_path = path.join(user_path, '.upiot')
    return upiot_path


def firmware_folder(board):
    """
    ~/.upiot/firmware/board
    """
    user_folder = upiot_user_folder()
    firmware_folder = path.join(user_folder, 'firmwares', board)
    return firmware_folder


def boards_folder():
    """
    Packages/uPIOT/boards
    """
    plugin_path = plugin_folder()
    boards_path = path.join(plugin_path, 'boards')
    return boards_path
