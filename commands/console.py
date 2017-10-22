import sublime
from sublime_plugin import WindowCommand

from ..tools import __version__
from ..tools import message
from ..tools import serial


class upiotConsoleCommand(WindowCommand):
    port = None
    txt = None

    def run(self):
        """Open/Stop serial console

        Opens the serial console in a new window or if it's already open,
        closes the connection to this, it wont close the message window.
        """
        txt = "uPIOT v{0}\nHelp, suggestion or error reports in\n" \
            "https: www.github.com/gepd/upiot\n===" \
            "".format(__version__)

        direction = 'self' if(self.check_empty_panel()) else 'down'

        # check the port selected
        self.port = serial.selected_port(request_port=True)

        if(not self.port):
            return

        # create and open the console window
        self.txt = message.Message(txt)
        if(not self.txt.recover_panel(self.port)):
            self.txt.create_panel(direction, extra_name=self.port)

        sublime.set_timeout_async(self.wait_console)

        # opens the console window
        sublime.active_window().run_command('upiot_console_write')

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

    def wait_console(self):
        """Open serial console

        Opens a panel (new file) and starts a serial connection in the selected
        port and show the data received in human readable format.
        """

        # Serial port connection
        link = serial.Serial(port=self.port, baudrate=115200)
        link.open()
        link.keep_listen(self.txt.print)
