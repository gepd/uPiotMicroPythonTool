import sublime
from subprocess import Popen
from sublime_plugin import WindowCommand

from .. import tools


class upiotAddProjectCommand(WindowCommand):

    def run(self, folder, append=False):
        data = self.window.project_data()

        if(not data):
            data = {}
            data["folders"] = []

        if(tools.check_sidebar_folder(folder)):
            return

        if(data and append):
            Popen([sublime.executable_path(), "-a", folder])
        else:
            new_folder = {}
            new_folder['path'] = folder
            data['folders'] = [new_folder]

        self.window.set_project_data(data)
