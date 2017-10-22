import sublime
from sublime_plugin import WindowCommand

from ..tools import paths
from .. import tools

setting_key = 'firmware_url'


class upiotDownloadFirmwareCommand(WindowCommand):
    url = None

    def run(self):
        self.window.show_input_panel('URL:', '', self.callback, None, None)

    def callback(self, url):
        """Firmware url

        Gets the url entered by the user and run the download method
        in a new thread

        Arguments:
            url {str} -- firmware url
        """
        self.url = url
        sublime.set_timeout_async(self.download_firmware, 0)

    def download_firmware(self):
        """Download firmware

        If the file isn't in the firmwares folder, it download the file and
        put it in a folder corresponding to the board selection
        """
        folder = paths.firmware_folder('esp32')
        tools.make_folder(folder)

        tools.ACTIVE_VIEW = self.window.active_view()
        out = tools.download_file(self.url, folder, callback=tools.set_status)

        if(out):
            tools.set_status('Download success')
        else:
            from os import path, remove

            filename = self.url.split('/')[-1]
            dst_path = path.join(folder, filename)
            remove(dst_path)

            tools.set_status('Error downloading')

        sublime.set_timeout_async(tools.clean_status, 2000)
