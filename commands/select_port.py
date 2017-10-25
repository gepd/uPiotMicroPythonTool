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
from ..tools.serial import ports_list

setting_key = 'serial_port'


class upiotSelectPortCommand(WindowCommand):
    items = []

    def run(self):
        self.items = ports_list()
        if(not self.items):
            self.items = ['No device found']
        tools.quick_panel(self.items, self.callback)

    def callback(self, selection):
        """Serial port callback

        Handles the serial port selection by the user

        Arguments:
            slection {int} -- index user selection
        """
        if(selection == -1):
            return

        port = self.items[selection]

        settings = sublime.load_settings(tools.SETTINGS_NAME)
        settings.set(setting_key, port)
        sublime.save_settings(tools.SETTINGS_NAME)
