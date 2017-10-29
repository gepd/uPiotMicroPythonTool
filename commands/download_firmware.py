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

from ..tools import paths
from .. import tools

setting_key = 'firmware_url'


class upiotDownloadFirmwareCommand(WindowCommand):
    url = None

    def run(self, selected=None):
        # selected board
        if(not selected):
            sublime.active_window().run_command('upiot_select_board',
                                                {'action': tools.DOWNLOAD})
            return

        self.window.show_input_panel('URL:', '', self.callback, None, None)

    def callback(self, url):
        """Firmware url

        Gets the url entered by the user and run the download method
        in a new thread

        Arguments:
            url {str} -- firmware url
        """
        self.url = url
        sublime.set_timeout_async(self.download_firmware, 0)

    def download_firmware(self):
        """Download firmware

        If the file isn't in the firmwares folder, it download the file and
        put it in a folder corresponding to the board selection
        """
        settings = sublime.load_settings(tools.SETTINGS_NAME)
        board = settings.get('board', None)
        folder = paths.firmware_folder(board)
        tools.make_folder(folder)

        tools.ACTIVE_VIEW = self.window.active_view()
        out = tools.download_file(self.url, folder, callback=tools.set_status)

        if(out):
            tools.set_status('Download success')
        else:
            from os import path, remove

            filename = self.url.split('/')[-1]
            dst_path = path.join(folder, filename)
            remove(dst_path)

            tools.set_status('Error downloading')

        sublime.set_timeout_async(tools.clean_status, 2000)
