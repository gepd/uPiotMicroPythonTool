# !/usr/bin/env python
# -*- coding: utf-8 -*-

from inspect import currentframe, getfile
from os import path, makedirs

#
# Plugin Paths
#

current_file = path.abspath(getfile(currentframe()))


def get_plugin():
    """
    Get absolute path of the plugin Packages/uPIOT
    """
    plugin_path = path.dirname(path.dirname(current_file))
    return plugin_path


def get_esptool():
    """
    Get the path of the esptool.py file
    """
    plugin_path = get_plugin()
    tools_path = path.join(plugin_path, 'tools', 'esptool.py')
    return tools_path


def get_user_upiot():
    """
    ~/.upiot/
    """
    user_path = path.expanduser('~')
    upiot_path = path.join(user_path, '.upiot')
    return upiot_path


def get_boards():
    """
    Packages/uPIOT/boards
    """
    plugin_path = get_plugin()
    boards_path = path.join(plugin_path, 'boards')
    return boards_path
