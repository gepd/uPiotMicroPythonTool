import sublime
from sublime_plugin import WindowCommand

from ..tools import ampy_manager
from ..tools.serial import selected_port


class upiotPutFileCommand(WindowCommand):

    def run(self):
        port = selected_port(request_port=True)
        if(not port):
            return

        self.window.show_input_panel('Path', '', self.callback, None, None)

    def callback(self, file):
        def put_file():
            ampy_manager.put_file(file)

        sublime.set_timeout_async(put_file, 0)
