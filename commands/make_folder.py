import sublime
from sublime_plugin import WindowCommand

from ..tools import sampy_manager
from ..tools.serial import selected_port


class upiotMakeFolderCommand(WindowCommand):

    def run(self):
        port = selected_port(request_port=True)
        if(not port):
            return

        self.window.show_input_panel('Name', '/', self.callback, None, None)

    def callback(self, folder_name):
        def make_folder():
            sampy_manager.make_folder(folder_name)
        sublime.set_timeout_async(make_folder, 0)
