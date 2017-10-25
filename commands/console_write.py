import sublime
from sublime_plugin import WindowCommand
from threading import Thread

from ..tools import serial


class upiotConsoleWriteCommand(WindowCommand):
    port = None

    def run(self):
        self.window.show_input_panel('>>>', '', self.callback, None, None)

    def callback(self, data):
        """Console write callback

        callback called after write any command in the ST input, if there
        is the 'sampy' prefix, a sampy (ampy) function will be call, otherwise
        the string enter will be write in the current serial connection

        Arguments:
            data {str} -- command to run or data to write
        """
        # check if there is a port available
        self.port = serial.selected_port(request_port=True)
        if(not self.port):
            return

        # run sampy commands
        if(data.startswith('sampy')):
            data = data.split()
            cmd = data[1]
            arg = data[2] if(len(data) > 2) else None

            th = Thread(target=self.sampy_commands, args=(cmd, arg))
            th.start()

            self.window.run_command('upiot_console_write')
            return

        # establish a connection if it doesn't exists
        if(self.port not in serial.in_use):
            serial.establish_connection(self.port)

        link = serial.serial_dict[self.port]
        link.writable(data)

        self.window.run_command('upiot_console_write')

    def sampy_commands(self, option, arg=None):
        """Console commands

        Executes the commands called from the console, this command
        are called with the 'sampy' prefix

        Arguments:
            option {str} -- command option (ls, run, get, etc)

        Keyword Arguments:
            arg {str} -- command argument required in some commands like
                        the filename (default: {None})
        """
        from ..tools import sampy_manager

        commands = {}

        commands['ls'] = sampy_manager.list_files
        commands['run'] = sampy_manager.run_file
        commands['get'] = sampy_manager.get_file
        commands['put'] = sampy_manager.put_file
        commands['rm'] = sampy_manager.remove_file
        commands['mkdir'] = sampy_manager.make_folder
        commands['rmdir'] = sampy_manager.remove_folder

        try:
            commands[option]()
        except:
            try:
                commands[option](arg)
            except:
                from ..tools import message
                txt = message.open(self.port)
                txt.print('\n\n>> CommandError: "{}" not found'.format(option))
