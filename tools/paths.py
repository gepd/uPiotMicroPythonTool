# !/usr/bin/env python
# -*- coding: utf-8 -*-

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
