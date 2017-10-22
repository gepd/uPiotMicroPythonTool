import sublime
from sublime_plugin import WindowCommand
from threading import Thread

from ..tools import serial


class upiotConsoleWriteCommand(WindowCommand):

    def run(self):
        self.window.show_input_panel('>>', '', self.callback, None, None)

    def callback(self, data):

        if(data.startswith('sampy')):
            data = data.split()
            cmd = data[1]
            arg = data[2] if(len(data) > 2) else None

            th = Thread(target=self.sampy_commands, args=(cmd, arg))
            th.start()

            self.window.run_command('upiot_console_write')
            return

        port = serial.selected_port()

        if(port in serial.in_use):
            link = serial.serial_dict[port]
            link.writable(data)

            self.window.run_command('upiot_console_write')

    def sampy_commands(self, option, arg=None):
        from ..tools import ampy_manager

        commands = {}

        commands['ls'] = ampy_manager.list_files
        commands['run'] = ampy_manager.run_file
        commands['get'] = ampy_manager.get_file
        commands['put'] = ampy_manager.put_file
        commands['rm'] = ampy_manager.remove_file
        commands['mkdir'] = ampy_manager.make_folder
        commands['rmdir'] = ampy_manager.remove_folder

        try:
            commands[option]()
        except:
            commands[option](arg)
