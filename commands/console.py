import sublime
from sublime_plugin import WindowCommand

from ..tools import __version__
from ..tools.message import Message
from ..tools import serial


class upiotConsoleCommand(WindowCommand):
    port = None

    def run(self):
        """Open/Stop serial console

        Opens the serial console in a new window or if it's already open,
        closes the connection to this, it wont close the message window.
        """
        self.port = serial.selected_port()

        if(self.port in serial.in_use):
            serial.serial_dict[self.port].close()
            return

        sublime.set_timeout_async(self.open_console)

        self.window.run_command('upiot_console_write')

    def check_empty_panel(self):
        """
        If there is an empty panel will make it active

        Returns:
            bool -- True if there is an empty panel false if not
        """
        num = self.window.num_groups()

        for n in range(0, num):
            if(not self.window.views_in_group(n)):
                self.window.focus_group(n)
                return True
        return False

    def open_console(self):
        """Open serial console

        Opens a panel (new file) and starts a serial connection in the selected
        port and show the data received in human readable format.
        """
        txt = "uPIOT v{0}\nHelp, suggestion ir error reports in\n" \
            "https: www.github.com/gepd/upiot\n===\n\n" \
            "".format(__version__)

        direction = 'self' if(self.check_empty_panel()) else 'down'

        message = Message(txt)
        message.create_panel(direction, extra_name=self.port)

        serial_o = serial.Serial(port=self.port, baudrate=115200)
        serial_o.open()

        while(serial_o.is_running()):
            data = serial_o.readable()
            message.print(data)
