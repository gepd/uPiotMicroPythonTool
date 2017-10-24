import sublime
from sublime_plugin import WindowCommand

from ..tools import sampy_manager
from ..tools import message
from threading import Thread
from ..tools.serial import selected_port


class upiotRunCurrentFileCommand(WindowCommand):

    def run(self):
        port = selected_port(request_port=True)
        if(not port):
            return

        view = self.window.active_view()
        file = view.file_name()

        if(not file):
            return

        if(view.is_dirty()):
            view.run_command('save')

        Thread(target=sampy_manager.run_file, args=(file,)).start()
