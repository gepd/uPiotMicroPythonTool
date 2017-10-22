import sublime
from sublime_plugin import WindowCommand

from ..tools import ampy_manager


class upiotRemoveFolderCommand(WindowCommand):

    def run(self):
        self.window.show_input_panel('Name', '/', self.callback, None, None)

    def callback(self, folder):
        def remove_folder():
            ampy_manager.remove_folder(folder)
        sublime.set_timeout_async(remove_folder, 0)
