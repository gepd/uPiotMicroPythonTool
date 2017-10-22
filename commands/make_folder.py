import sublime
from sublime_plugin import WindowCommand

from ..tools import ampy_manager


class upiotMakeFolderCommand(WindowCommand):

    def run(self):
        self.window.show_input_panel('Name', '/', self.callback, None, None)

    def callback(self, folder_name):
        def make_folder():
            ampy_manager.make_folder(folder_name)
        sublime.set_timeout_async(make_folder, 0)
