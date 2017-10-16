from __future__ import absolute_import

from sublime import platform
from . import pyserial
from .pyserial.tools import list_ports


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
