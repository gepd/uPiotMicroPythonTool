import sublime
from sublime_plugin import WindowCommand
from threading import Thread
from ..tools import ampy_manager
from ..tools.serial import selected_port


class upiotRetrieveAllFilesCommand(WindowCommand):

    def run(self):
        port = selected_port(request_port=True)
        if(not port):
            return

        self.window.show_input_panel(
            'Destination:', '', self.callback, None, None)

    def callback(self, path):
        Thread(target=ampy_manager.get_files, args=(path,)).start()
