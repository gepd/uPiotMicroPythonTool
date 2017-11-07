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
from threading import Thread

from ..tools import serial


class upiotConsoleWriteCommand(WindowCommand):
    port = None

    def run(self):
        self.window.show_input_panel('>>>', '', self.callback, None, None)

    def callback(self, data):
        """Console write callback

        callback called after write any command in the ST input, if there
        is the 'sampy' prefix, a sampy (ampy) function will be call, otherwise
        the string enter will be write in the current serial connection

        Arguments:
            data {str} -- command to run or data to write
        """
        # check if there is a port available
        self.port = serial.selected_port(request_port=True)
        if(not self.port):
            return

        # run sampy commands
        if(data.startswith(('sampy', '--help'))):
            data = data.split()
            try:
                cmd = data[1]
            except IndexError:
                cmd = data[0]

            arg = data[2] if(len(data) > 2) else None

            th = Thread(target=self.sampy_commands, args=(cmd, arg))
            th.start()

            self.window.run_command('upiot_console_write')
            return

        # establish a connection if it doesn't exists
        if(self.port not in serial.in_use):
            serial.establish_connection(self.port)

        link = serial.serial_dict[self.port]

        # destroy connection
        if(data == '--close'):
            from ..tools import message

            link.disconnect()
            link.destroy()

            txt = message.open(self.port)
            txt.print("\n\nConnection to port {0} closed.".format(self.port))
            return

        link.writable(data)

        self.window.run_command('upiot_console_write')

    def sampy_commands(self, option, arg=None):
        """Console commands

        Executes the commands called from the console, this command
        are called with the 'sampy' prefix

        Arguments:
            option {str} -- command option (ls, run, get, etc)

        Keyword Arguments:
            arg {str} -- command argument required in some commands like
                        the filename (default: {None})
        """
        from ..tools import sampy_manager

        commands = {}

        commands['ls'] = sampy_manager.list_files
        commands['run'] = sampy_manager.run_file
        commands['get'] = sampy_manager.get_file
        commands['put'] = sampy_manager.put_file
        commands['rm'] = sampy_manager.remove_file
        commands['mkdir'] = sampy_manager.make_folder
        commands['rmdir'] = sampy_manager.remove_folder
        commands['--help'] = sampy_manager.help

        try:
            commands[option]()
        except:
            try:
                commands[option](arg)
            except KeyError:
                from ..tools import message
                txt = message.open(self.port)
                txt.print('\n\n>> CommandError: "{}" not found'.format(option))
