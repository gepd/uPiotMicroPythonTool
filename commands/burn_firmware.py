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

from glob import glob
from json import loads
from os.path import join, basename

from .. import tools
from ..tools import paths
from ..tools import serial

setting_key = 'board'


class upiotBurnFirmwareCommand(WindowCommand):
    board = None
    port = None
    items = None
    firmwares = None
    url = None

    def run(self, selected=None):
        # only continue if a device is available
        self.port = serial.selected_port(request_port=True)
        if(not self.port):
            return

        self.items = []

        settings = sublime.load_settings(tools.SETTINGS_NAME)
        self.board = settings.get(setting_key, None)

        if(not selected):
            sublime.active_window().run_command('upiot_select_board',
                                                {'action': tools.BURN})
            return

        self.firmwares = paths.firmware_folder(self.board)
        self.firmware_list()

        tools.quick_panel(self.items, self.callback_selection)

    def callback_selection(self, selection):
        """Firmware selection

        Receive the user selection and run the burn process
        in a new thread

        Arguments:
            selection {int} -- user index selection
        """
        if(selection == -1):
            return

        self.url = self.items[selection]
        sublime.set_timeout_async(self.burn_firmware, 0)

    def firmware_list(self):
        """Firmware files list

        Lis of file in the firmwares folder
        """
        firm_path = join(self.firmwares, '*')

        # file names who shouldn't be displayed in the list
        blacklist = [
                        'flash.sh',
                        'bootloader',
                        'bootloader.bin',
                        'partitions_mpy.bin',
                        'partitions_mpy.csv',
                        'phy_init_data.bin'
                    ]

        for firmware in glob(firm_path):
            name = basename(firmware)
            if(name not in blacklist):
                self.items.append(name)

    def burn_firmware(self):
        """Burn firmware

        Uses esptool.py to burn the firmware
        """
        from ..tools.command import Command

        filename = self.url.split('/')[-1]
        firmware = join(self.firmwares, filename)

        options = self.get_board_options()
        options.append(firmware)

        caption = "Do you want to erase the flash memory?"
        answer = sublime.yes_no_cancel_dialog(caption, "Yes", "No")

        # stop
        if(answer == sublime.DIALOG_CANCEL):
            return

        # erase flash
        if(answer == sublime.DIALOG_YES):
            tools.erase_flash()

        options.insert(0, "--port " + self.port)

        if(not serial.check_port(self.port)):
            return

        if(self.port in serial.in_use):
            serial.serial_dict[self.port].disconnect()

        Command().run(options, port=self.port)

    def get_board_options(self):
        """get board option

        get the options defined in the json board file

        Returns:
            list -- board options
        """
        board_folder = paths.boards_folder()
        filename = self.board + '.json'
        board_path = join(board_folder, filename)

        board_file = []
        with open(board_path) as file:
            board_file = loads(file.read())

        options = []
        for key, value in board_file['upload'].items():
            if('write_flash' not in key):
                separator = '' if key.endswith('=') else ' '
                option = "{0}{1}{2}".format(key, separator, value)
                options.append(option)

        wf = board_file['upload']['write_flash']
        wf = wf.format(self.firmwares)
        options.append('write_flash ' + wf)

        return options
