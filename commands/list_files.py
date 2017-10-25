import sublime
from sublime_plugin import WindowCommand

from ..tools import sampy_manager
from ..tools.serial import selected_port


class upiotListFilesCommand(WindowCommand):

    def run(self):
        port = selected_port(request_port=True)
        if(not port):
            return

        sublime.set_timeout_async(sampy_manager.list_files, 0)
