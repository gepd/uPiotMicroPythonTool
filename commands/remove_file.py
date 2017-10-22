import sublime
from sublime_plugin import WindowCommand

from ..tools import ampy_manager


class upiotRemoveFileCommand(WindowCommand):

    def run(self):
        self.window.show_input_panel('Path', '', self.callback, None, None)

    def callback(self, file):
        def remove_file():
            ampy_manager.remove_file(file)

        sublime.set_timeout_async(remove_file, 0)
