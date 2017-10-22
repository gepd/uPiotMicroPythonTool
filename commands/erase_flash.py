import sublime
from sublime_plugin import WindowCommand

from .. import tools


class upiotEraseFlashCommand(WindowCommand):

    def run(self):
        # show console
        tools.show_console()

        sublime.set_timeout_async(tools.erase_flash, 0)
