import sublime
from sublime_plugin import WindowCommand

from .. import tools
from ..tools.pserial import ports_list

setting_key = 'serial_port'


class upiotSelectPortCommand(WindowCommand):
    items = []

    def run(self):
        self.items = ports_list()
        if(not self.items):
            self.items = ['No serial port was found']
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
        sublime.save_sttings(tools.SETTINGS_NAME)
