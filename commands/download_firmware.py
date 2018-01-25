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
from time import time
from sublime_plugin import WindowCommand
from os import path, remove, rename
from datetime import datetime

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
        tools.ACTIVE_VIEW = self.window.active_view()
        tools.set_status('Preparing download')

        settings = sublime.load_settings(tools.SETTINGS_NAME)
        board = settings.get('board', None)
        folder = paths.firmware_folder(board)
        tools.make_folder(folder)

        filename = self.url.split('/')[-1]
        destination = path.join(folder, filename)

        out = tools.download_file(self.url, destination, callback=tools.set_status)

        if(out):
            tools.set_status('Download success')
            self.extract_file(destination, folder)            
        else:
            remove(destination)
            tools.set_status('Error downloading')

        sublime.set_timeout_async(tools.clean_status, 2000)


    def extract_file(self, filepath, destination):
        tools.set_status('Extracting file...')

        cur_datetime = datetime.now().strftime("%y%m%d-%H%M")
        extension = filepath.split(".")[-1]
        zip_name = path.basename(filepath).split(".")[0]
        
        if(extension not in ['zip', 'gz', 'bz2']):
            return

        if(extension in ['gz', 'bz2']):
            import tarfile

            tar = tarfile.open(filepath, 'r:' + extension)
            for item in tar:
                tar.extract(item, destination)

        if(extension in ['zip']):
            import zipfile

            with zipfile.ZipFile(filepath, 'r') as file:
                file.extractall(destination)

        # new name based in the current time to avoid collition with futures downloads
        extracted_folder = path.join(destination, 'esp32')
        if(path.isdir(extracted_folder)):
            rename(extracted_folder, path.join(destination, zip_name))

        # rename MicroPython.bin to datetime based name
        micropython = path.join(destination, zip_name, 'MicroPython.bin')
        new_name = path.join(destination, zip_name, cur_datetime + '.bin')
        if(path.isfile(micropython)):
            rename(micropython, new_name)

        remove(filepath)

        

        