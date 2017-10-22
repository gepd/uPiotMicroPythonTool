import sublime
from sublime_plugin import WindowCommand

from ..tools import ampy_manager


class upiotPutCurrentFileCommand(WindowCommand):

    def run(self):
        file = self.window.active_view().file_name()

        def put_file():
            ampy_manager.put_file(file)

        sublime.set_timeout_async(put_file, 0)
