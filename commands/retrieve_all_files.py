import sublime
from sublime_plugin import WindowCommand
from threading import Thread
from ..tools import ampy_manager


class upiotRetrieveAllFilesCommand(WindowCommand):

    def run(self):
        self.window.show_input_panel(
            'Destination:', '', self.callback, None, None)

    def callback(self, path):
        Thread(target=ampy_manager.get_files, args=(path,)).start()
