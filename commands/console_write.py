import sublime
from sublime_plugin import WindowCommand

from ..tools import serial


class upiotConsoleWriteCommand(WindowCommand):

    def run(self):
        self.window.show_input_panel('>>', '', self.callback, None, None)

    def callback(self, data):
        port = serial.selected_port()

        if(port in serial.in_use):
            serial_o = serial.serial_dict[port]
            serial_o.writable(data)

        self.window.run_command('upiot_console_write')
