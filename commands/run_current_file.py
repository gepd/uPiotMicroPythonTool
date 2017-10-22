import sublime
from sublime_plugin import WindowCommand

from ..tools import ampy_manager
from ..tools import message
from threading import Thread


class upiotRunCurrentFileCommand(WindowCommand):

    def run(self):

        view = self.window.active_view()
        file = view.file_name()

        if(not file):
            return

        if(view.is_dirty()):
            view.run_command('save')

        Thread(target=ampy_manager.run_file, args=(file,)).start()
