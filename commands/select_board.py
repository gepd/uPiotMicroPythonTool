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

from .. import tools
from ..tools import boards

setting_key = 'board'


class upiotSelectBoardCommand(WindowCommand):
    items = []
    action = None

    def run(self, action):
        self.action = action
        self.items = boards.boards_list()

        if(not self.items):
            self.items = ['No boards found']
        tools.quick_panel(self.items, self.callback)

    def callback(self, selection):
        """Serial port callback

        Handles the serial port selection by the user

        Arguments:
            slection {int} -- index user selection
        """
        if(selection == -1):
            return

        board = self.items[selection]

        settings = sublime.load_settings(tools.SETTINGS_NAME)
        settings.set(setting_key, board)
        sublime.save_settings(tools.SETTINGS_NAME)

        if(self.action == tools.BURN):
            sublime.active_window().run_command(
                'upiot_burn_firmware', {'selected': True})
        elif(self.action == tools.DOWNLOAD):
            sublime.active_window().run_command(
                'upiot_download_firmware', {'selected': True})
