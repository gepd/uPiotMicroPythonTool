import sublime
from sublime_plugin import WindowCommand

from ..tools import __version__
from ..tools import message
from ..tools import serial


class upiotConsoleCommand(WindowCommand):

    def run(self):
        """Open/Stop serial console

        Opens the serial console in a new window or if it's already open,
        closes the connection to this, it wont close the message window.
        """
        # check the port selected
        port = serial.selected_port(request_port=True)

        if(not port):
            return

        # create and open the console window
        serial.establish_connection(port)

        # opens the console window
        sublime.active_window().run_command('upiot_console_write')
