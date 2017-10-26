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

import sublime
from sublime_plugin import WindowCommand

from .. import requests
from os import path, makedirs

from ..tools.boards import boards_list
from ..tools.quick_panel import quick_panel

VERSION = (0, 0, 1)
ACTIVE_VIEW = None

global SETTINGS_NAME
SETTINGS_NAME = 'upiot.sublime-settings'


def versionize(raw_version):
    """Semantic Versioning

    Convert the given version in the semantic versioning format

    Arguments:
       raw_version {tuple} -- plugin version in a tuple

    Returns:
       [str] -- Semantic Versioning string
    """
    version = ".".join([str(s) for s in raw_version[:3]])
    if(len(raw_version) > 3):
        version += raw_version[3]
    return version

__all__ = ["boards_list",
           "run_command",
           "quick_panel"]


def get_headers():
    """
    headers for urllib request
    """

    user_agent = 'uPIOT/{0} (Sublime-Text/{1})'.format(__version__,
                                                       sublime.version())
    headers = {'User-Agent': user_agent}
    return headers


def download_file(file_url, dst_path, callback=None):
    """download file

    Download and save a file from a given url

    Arguments:
       file_url {str} -- url with the file to download
       dst_path {str} -- where file will be stored
       callback {obj} -- callback to show the progress of the download

    Returns:
        bool -- true if the file was successfully downloaded
    """
    downloaded = 0
    progress_qty = 5  # numbers of symbols to show when it downloading (total)
    headers = get_headers()
    filename = file_url.split('/')[-1]
    dst_path = path.join(dst_path, filename)

    # stop if the file already exits
    if(path.exists(dst_path)):
        return True

    with open(dst_path, 'wb') as file:
        try:
            req = requests.get(file_url, stream=True, headers=headers)
        except:
            return False

        total_length = req.headers.get('content-length')

        # File status
        if(req.status_code != 200):
            return False

        if total_length is None:
            file.write(req.content)
        else:
            for chunk in req.iter_content(1024):
                downloaded += len(chunk)
                file.write(chunk)
                done = int(progress_qty * downloaded / int(total_length))
                percent = int(100 * downloaded) / int(total_length)

                if(callback):
                    current_prog = '■' * done
                    new_prog = '   ' * (progress_qty - done)
                    callback("Downloading Firmware {0:.0f}% [{1}{2}]".format(
                        percent, current_prog, new_prog))
        return True


def erase_flash():
    """Erase flash memory

    Erase the flash memory from the current selected device
    """
    from ..tools.command import Command
    from ..tools import serial

    port = serial.selected_port(request_port=True)
    if(not port):
        return

    options = ['--port', port, 'erase_flash']
    Command().run(options)


def make_folder(folder_path):
    """make foler

    Make a folder in the given path

    Arguments:
        folder_path {str} -- folder to make

    Raises:
        exc -- [description]
    """
    if(not path.exists(folder_path)):
        import errno

        try:
            makedirs(folder_path)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise exc
            pass


def find_view(view_name):
    """
    Search a specific view in the list of available views

    Arguments:
        view_name {string}
            Name of the view to search
    """
    opened_view = None
    found = False
    fwindows = sublime.windows()
    for window in fwindows:
        views = window.views()
        for view in views:
            name = view.name()
            if(view_name in name):
                opened_view = view
                found = True
                break
        if found:
            break
    return (window, opened_view)


def check_sidebar_folder(folder):
    """check folder in sidebar

    Checks if the given folder already is in the current project

    Arguments:
        folder {str} -- folder to search

    Returns:
        bool -- true if already is false if not
    """
    data = sublime.active_window().project_data()
    if(not data):
        return False
    else:
        paths = [path['path'] for path in data["folders"]]
        if(folder in paths):
            return True
        return False


def set_status(text):
    """Set the status bar

    Sets a message/text in the status bar

    Arguments:
        text {str} -- text to add
    """
    if(ACTIVE_VIEW):
        ACTIVE_VIEW.set_status('_upiot_', text)


def clean_status():
    """Remove status bar text

    Removes the status bar text related to the plugin
    """
    if(ACTIVE_VIEW):
        ACTIVE_VIEW.erase_status('_upiot_')


def show_console():
    """Open ST console

    Opens the Sublime Text console
    """
    options = {'panel': 'console', 'toggle': True}
    sublime.active_window().run_command('show_panel', options)

__version__ = versionize(VERSION)
