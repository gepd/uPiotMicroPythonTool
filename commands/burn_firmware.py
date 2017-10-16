import sublime
from sublime_plugin import WindowCommand

from glob import glob
from json import loads
from os.path import join, basename

from .. import tools
from ..tools import paths
from ..tools import pserial

setting_key = 'serial_ports'


class upiotBurnFirmwareCommand(WindowCommand):
    items = None
    firmwares = None
    url = None

    def run(self):
        self.items = []
        self.firmwares = paths.firmware_folder('esp32')
        self.firmware_list()

        tools.quick_panel(self.items, self.callback_selection)

    def callback_selection(self, selection):
        """Firmware selection

        Receive the user selection and run the burn process
        in a new thread

        Arguments:
            selection {int} -- user index selection
        """
        if(selection == -1):
            return

        self.url = self.items[selection]
        sublime.set_timeout_async(self.burn_firmware, 0)

    def firmware_list(self):
        """Firmware files list

        Lis of file in the firmwares folder
        """
        firm_path = join(self.firmwares, '*')

        for firmware in glob(firm_path):
            name = basename(firmware)
            self.items.append(name)

    def burn_firmware(self):
        """Burn firmware

        Uses esptool.py to burn the firmware
        """
        filename = self.url.split('/')[-1]
        firmware = join(self.firmwares, filename)

        options = self.get_board_options('esp32')
        options.append(firmware)

        port = self.get_serial_port()
        if(not port):
            return

        options.insert(0, "--port " + port)

        # show console
        self.window.run_command(
            'show_panel', {'panel': 'console', 'toggle': True})

        if(not pserial.check_port(port)):
            return

        tools.run_command(options)

    @staticmethod
    def get_board_options(board):
        """get board option

        get the options defined in the json board file

        Arguments:
            board {str} -- board selected

        Returns:
            list -- board options
        """
        board_folder = paths.boards_folder()
        filename = board + '.json'
        board_path = join(board_folder, filename)

        board_file = []
        with open(board_path) as file:
            board_file = loads(file.read())

        options = []
        for key, value in board_file['upload'].items():
            if('write_flash' not in key):
                separator = '' if key.endswith('=') else ' '
                option = "{0}{1}{2}".format(key, separator, value)
                options.append(option)

        wf = board_file['upload']['write_flash']
        options.append('write_flash ' + wf)

        return options

    def get_serial_port(self):
        ports = pserial.ports_list()
        if(ports):
            items = []
            for port in ports:
                items.append(port[1])
            ports = items

        settings = sublime.load_settings(tools.SETTINGS_NAME)
        port_setting = settings.get(setting_key, None)

        if(ports and len(ports) == 1):
            return ports[0]
        elif(ports and len(ports) == 0):
            return None
        elif(not port_setting):
            self.window.run_command('upiot_select_port')
            return False
        elif(port_setting not in ports):
            self.window.run_command('select_port')
            return False

        return port_setting
