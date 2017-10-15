from os.path import split, join
from sublime_plugin import WindowCommand
from sublime import set_timeout_async
from .. import tools
from ..tools import paths


class UpiotDownloadBurnFirmwareCommand(WindowCommand):

    def run(self):
        set_timeout_async(self.download_firmware, 0)

    def download_firmware(self):
        file_url = "http://micropython.org/resources/firmware/" \
            "esp32-20171015-v1.9.2-277-gd7b373c6.bin"

        dst_path = paths.get_user_upiot()
        tools.make_folder(dst_path)

        tools.ACTIVE_VIEW = self.window.active_view()

        tools.download_file(file_url, dst_path, callback=tools.set_status)
        set_timeout_async(tools.clean_status, 2000)

        filename = file_url.split('/')[-1]
        firmware = join(dst_path, filename)

        options = ['--chip esp32',
                   '--port COM3',
                   '--baud 460800',
                   'write_flash -z',
                   '0x1000',
                   firmware]

        run_command(options)
