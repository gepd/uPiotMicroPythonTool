import sublime
from sublime_plugin import WindowCommand

from ..tools import ampy_manager
from ..tools.serial import selected_port


class upiotRemoveFileCommand(WindowCommand):

    def run(self):
        port = selected_port(request_port=True)
        if(not port):
            return

        self.window.show_input_panel('Path', '', self.callback, None, None)

    def callback(self, file):
        def remove_file():
            ampy_manager.remove_file(file)

        sublime.set_timeout_async(remove_file, 0)
