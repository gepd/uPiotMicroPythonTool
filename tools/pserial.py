from __future__ import absolute_import

from sublime import platform
from . import pyserial
from .pyserial.tools import list_ports

setting_key = 'serial_ports'


def ports_list():
    """List of serial ports

    Return the list of serial ports availables on the system.

    Returns:
        [list/list] -- list of list like [['port1 fullname',
                       port_name]['port2 fullname', 'port_name']]
    """
    ports = list(list_ports.comports())
    dev_names = ['ttyACM', 'ttyUSB', 'tty.', 'cu.']

    serial_ports = []
    for port_no, description, address in ports:
        for dev_name in dev_names:
            if(address != 'n/a' and
                    dev_name in port_no or platform() == 'windows'):
                serial_ports.append([description, port_no])
                break

    return serial_ports


def check_port(port):
    """Check serial port

    Checks if the given serial port exits or if isn't busy

    Arguments:
        port {str} -- serial port name

    Returns:
        bool -- True if exist/not busy False if not
    """
    serial = pyserial.Serial()
    serial.port = port

    try:
        serial.open()
    except pyserial.serialutil.SerialException as e:
        if('PermissionError' in str(e)):
            print("Your port is busy")
            return False
        elif('FileNotFoundError' in str(e)):
            print("Port not found")
            return False
    return True


def get_serial_port():
    """Get serial port

    If there is only one port available, it will be automatically used,
    even if it is not in the preferences, if there is more than one port,
    the user selection will be used, if not setting stored or it's outdated
    one, the user will prompted to select one.

    Returns:
        str -- selected port, false with any problem
    """
    ports = ports_list()
    if(ports):
        items = []
        for port in ports:
            items.append(port[1])
        ports = items

    settings = sublime.load_settings(SETTINGS_NAME)
    port_setting = settings.get(setting_key, None)

    if(ports and len(ports) == 1):
        return ports[0]
    elif(ports and len(ports) == 0):
        return False
    elif(not port_setting):
        sublime.active_window().run_command('upiot_select_port')
        return False
    elif(port_setting not in ports):
        sublime.active_window().run_command('select_port')
        return False

    return port_setting
