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
from sublime_plugin import EventListener

import collections
import threading

from .. import tools

session = None
close_panel = False
viewer_name = '$ Micropython Viewer'


class Message:
    BLOCK_SIZE = 2 ** 14
    text_queue = collections.deque()
    text_queue_lock = threading.Lock()

    def __init__(self, init_text=None):
        self._init_text = init_text

    def create_panel(self, direction='down', extra_name=None):
        """
        Start the print module, if the window was already created
        it's recovered.
        """
        global session
        global viewer_name

        # Update viewer_name with extra info if it exists
        edit_view_name(extra_name)

        # check if the windows was already created
        # self.recover_output()

        self.output_view = new_file_panel(direction)

        # print initial message
        if(self._init_text):
            self.print(self._init_text)

        session = self

    def print(self, text):
        """
        Adds the string in the deque list
        """
        self.text_queue_lock.acquire()
        try:
            self.text_queue.append(text)
        finally:
            self.text_queue_lock.release()

        sublime.set_timeout(self.service_text_queue, 0)

    def service_text_queue(self):
        """
        Handles the deque list to print the messages
        """
        self.text_queue_lock.acquire()

        is_empty = False
        try:
            if(len(self.text_queue) == 0):
                return

            characters = self.text_queue.popleft()
            is_empty = (len(self.text_queue) == 0)

            self.send_to_file(characters)

        finally:
            self.text_queue_lock.release()

        if(not is_empty):
            sublime.set_timeout(self.service_text_queue, 1)

    def send_to_file(self, text):
        """
        Prints the text in the window
        """
        self.output_view.set_read_only(False)
        self.output_view.run_command('append', {'characters': text})
        self.output_view.set_read_only(True)
        if(text.rstrip()):
            self.output_view.run_command(
                "move_to", {"extend": True, "to": "eof"})

    def recover_panel(self, port):
        """
        Recover the message window object
        """
        global session

        edit_view_name(port)

        window, view = self.get_message_winview()

        if(view):
            self.output_view = view

            session = self
            return True
        return False

    @staticmethod
    def get_message_winview():
        """Window and view from message viewer

        Gets the window and view sublime text object from the message
        viewer.

        Returns:
            obj, obj -- window, view
        """
        global viewer_name

        return tools.find_view(viewer_name)

    def check_message_group(port):
        """Get message view group

        Gets the group number of the message view before close it
        """
        global group_index
        global viewer_name

        # add the port name in the view name
        edit_view_name(port)

        window, view = tools.find_view(viewer_name)

        if(view and viewer_name in view.name()):
            group_index = window.get_view_index(view)[0]


class CloseConsole(EventListener):

    def on_pre_close(self, view):
        """Check console panel

        Checks if the panel closed is the console or not and store it
        in a global var

        Arguments:
            view {obj} -- Sublime Text View
        """
        global viewer_name
        global close_panel

        if(viewer_name in view.name()):
            close_panel = True

    def on_close(self, view):
        """Close console close

        If the panel was identified as console panel, it will be closed

        Arguments:
            view {obj} -- Sublime Text View
        """
        global close_panel

        if(close_panel):
            window = sublime.active_window()
            active_group = window.active_group()

            if len(window.views_in_group(active_group)) == 0:
                window.run_command("destroy_pane", args={"direction": "self"})
        close_panel = False


def open(port):
    """Start the message deque

    If there is a panel already opened in ST and the device is connected, it
    will recover the session and start the printer in that window otherwise
    will create a new panel and return the message instance

    Arguments:
        port {str} -- port to open

    Returns:
        obj -- Message class instance
    """
    if(Message().recover_panel(port)):
        txt = session
    else:
        from ..tools import __version__

        head = """
            *******************************
            UPIOT v{} uPython Tool
            *******************************

            Use sampy --help to get a list of the available commands.

            https://github.com/gepd/uPiotMicroPythonTool for help, suggetions
            or bug report.
            ---
            """.replace('    ', '').format(__version__)

        direction = 'self' if(check_empty_panel()) else 'down'

        txt = Message(head)
        txt.create_panel(direction=direction, extra_name=port)
    return txt


def check_empty_panel():
    """
    If there is an empty panel will make it active

    Returns:
        bool -- True if there is an empty panel false if not
    """
    from sublime import active_window

    window = active_window()
    num = window.num_groups()

    for n in range(0, num):
        if(not window.views_in_group(n)):
            window.focus_group(n)
            return True
    return False


def new_file_panel(direction):
    """Create an empty new file sheet

    Creates an empty sheet to be used as console

    Arguments:
        direction {str} -- Where the window will be located. options available:
                            'self', 'left', 'right', 'up', 'down'

    Returns:
        obj -- Sublime Text view buffer
    """
    window = sublime.active_window()

    word_wrap = {'setting': 'word_wrap'}
    options = {'direction': direction, 'give_focus': True}

    window.run_command('upiot_create_pane', options)

    view = window.new_file()
    view.set_name(viewer_name)
    view.run_command('toggle_setting', word_wrap)
    view.set_scratch(True)

    return view


def edit_view_name(text):
    """Edit viewer name

    Edits the viewer name global vtar

    Arguments:
        text {str} -- text to adds in the viewer window name
    """
    global viewer_name

    if(text and text not in viewer_name):
        viewer_name = '{} | {}'.format(viewer_name, text)
