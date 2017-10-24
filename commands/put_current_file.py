import sublime
from sublime_plugin import WindowCommand

from ..tools import sampy_manager
from ..tools.serial import selected_port


class upiotPutCurrentFileCommand(WindowCommand):

    def run(self):
        port = selected_port(request_port=True)
        if(not port):
            return

        file = self.window.active_view().file_name()

        def put_file():
            sampy_manager.put_file(file)

        sublime.set_timeout_async(put_file, 0)
