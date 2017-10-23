import sublime
from sublime_plugin import WindowCommand

from .. import tools
from ..tools import boards

setting_key = 'board'


class upiotSelectBoardCommand(WindowCommand):
    items = []

    def run(self):
        self.items = boards.boards_list()
        if(not self.items):
            self.items = ['No boards found']
        tools.quick_panel(self.items, self.callback)

    def callback(self, selection):
        """Serial port callback

        Handles the serial port selection by the user

        Arguments:
            slection {int} -- index user selection
        """
        if(selection == -1):
            return

        board = self.items[selection]

        settings = sublime.load_settings(tools.SETTINGS_NAME)
        settings.set(setting_key, board)
        sublime.save_settings(tools.SETTINGS_NAME)

        sublime.active_window().run_command(
            'upiot_burn_firmware', {'selected': True})
