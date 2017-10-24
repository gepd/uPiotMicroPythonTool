import sublime
from sublime_plugin import WindowCommand

from ..tools import sampy_manager
from ..tools.serial import selected_port


class upiotRemoveFolderCommand(WindowCommand):

    def run(self):
        port = selected_port(request_port=True)
        if(not port):
            return

        self.window.show_input_panel('Name', '/', self.callback, None, None)

    def callback(self, folder):
        def remove_folder():
            sampy_manager.remove_folder(folder)
        sublime.set_timeout_async(remove_folder, 0)
