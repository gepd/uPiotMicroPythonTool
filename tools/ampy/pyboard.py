#!/usr/bin/env python

"""
pyboard interface

This module provides the Pyboard class, used to communicate with and
control the pyboard over a serial USB connection.

Example usage:

    import pyboard
    pyb = pyboard.Pyboard('/dev/ttyACM0')

Or:

    pyb = pyboard.Pyboard('192.168.1.1')

Then:

    pyb.enter_raw_repl()
    pyb.exec('pyb.LED(1).on()')
    pyb.exit_raw_repl()

Note: if using Python2 then pyb.exec must be written as pyb.exec_.
To run a script from the local machine on the board and print out the results:

    import pyboard
    pyboard.execfile('test.py', device='/dev/ttyACM0')

This script can also be run directly.  To execute a local script, use:

    ./pyboard.py test.py

Or:

    python pyboard.py test.py

"""

import sys
import time

in_use = []
serial_dict = {}


class PyboardError(BaseException):
    pass


class TelnetToSerial:

    def __init__(self, ip, user, password, read_timeout=None):
        import telnetlib
        self.tn = telnetlib.Telnet(ip, timeout=15)
        self.read_timeout = read_timeout
        if b'Login as:' in self.tn.read_until(b'Login as:', timeout=read_timeout):
            self.tn.write(bytes(user, 'ascii') + b"\r\n")

            if b'Password:' in self.tn.read_until(b'Password:', timeout=read_timeout):
                # needed because of internal implementation details of the
                # telnet server
                time.sleep(0.2)
                self.tn.write(bytes(password, 'ascii') + b"\r\n")

                if b'for more information.' in self.tn.read_until(b'Type "help()" for more information.', timeout=read_timeout):
                    # login succesful
                    from collections import deque
                    self.fifo = deque()
                    return

        raise PyboardError(
            'Failed to establish a telnet connection with the board')

    def __del__(self):
        self.close()

    def close(self):
        self.data_consumer("closed")
        try:
            self.tn.close()
        except:
            # the telnet object might not exist yet, so ignore this one
            pass

    def read(self, size=1):
        while len(self.fifo) < size:
            timeout_count = 0
            data = self.tn.read_eager()
            if len(data):
                self.fifo.extend(data)
                timeout_count = 0
            else:
                time.sleep(0.25)
                if self.read_timeout is not None and timeout_count > 4 * self.read_timeout:
                    break
                timeout_count += 1

        data = b''
        while len(data) < size and len(self.fifo) > 0:
            data += bytes([self.fifo.popleft()])
        return data

    def write(self, data):
        self.tn.write(data)
        return len(data)

    def inWaiting(self):
        n_waiting = len(self.fifo)
        if not n_waiting:
            data = self.tn.read_eager()
            self.fifo.extend(data)
            return len(data)
        else:
            return n_waiting


class Pyboard:
    port = None
    data_consumer = None

    def __init__(self, oserial, user='micro', password='python', data_consumer=None):
        self.data_consumer = data_consumer
        self.serial = oserial

    def write(self, data):
        self.serial.write(data)

    def read_until(self, min_num_bytes, ending, timeout=10):
        frepl = b'Type "help()" for more information'
        data = self.serial.read(min_num_bytes)

        timeout_count = 0
        while True:
            if data.endswith(ending):
                break
            if data.endswith(frepl):
                data = b''
                # ctrl-A: enter raw REPL
                self.serial.write(b'\r\x01')
            elif self.serial.inWaiting() > 0:
                new_data = self.serial.read(1)
                data = data + new_data
                timeout_count = 0
            else:
                timeout_count += 1
                if timeout is not None and timeout_count >= 100 * timeout:
                    break
                time.sleep(0.01)

        return data

    def enter_raw_repl(self):
        # ctrl-C twice: interrupt any running program
        self.serial.write(b'\r\x03\x03')
        self.serial.write(b'\x04')

        # flush input (without relying on serial.flushInput())
        n = self.serial.inWaiting()
        while n > 0:
            self.serial.read(n)
            n = self.serial.inWaiting()

        self.serial.write(b'\r\x01')  # ctrl-A: enter raw REPL
        data = self.read_until(1, b'raw REPL; CTRL-B to exit\r\n>')
        if not data.endswith(b'raw REPL; CTRL-B to exit\r\n>'):
            print(data)
            raise PyboardError('could not enter raw repl')

        self.serial.write(b'\x04')  # ctrl-D: soft reset
        data = self.read_until(1, b'soft reboot\r\n')
        if not data.endswith(b'soft reboot\r\n'):
            print(data)
            raise PyboardError('could not enter raw repl')

        # By splitting this into 2 reads, it allows boot.py to print stuff,
        # which will show up after the soft reboot and before the raw REPL.
        # Modification from original pyboard.py below:
        # Add a small delay and send Ctrl-C twice after soft reboot to ensure
        # any main program loop in main.py is interrupted.

        time.sleep(0.5)

        # interrupt any running program
        self.serial.write(b'\x03\x03')

        # End modification above.
        data = self.read_until(1, b'raw REPL; CTRL-B to exit\r\n')
        if not data.endswith(b'raw REPL; CTRL-B to exit\r\n'):
            print(data)
            raise PyboardError('could not enter raw repl')

    def exit_raw_repl(self):
        # ctrl-B: enter friendly REPL
        self.serial.write(b'\r\x02')

    def eval(self, expression, quiet=False):
        ret = self.exec_('print({})'.format(expression))
        ret = ret.strip()
        return ret

    def exec_(self, command, quiet=True):
        if isinstance(command, bytes):
            command_bytes = command
        else:
            command_bytes = bytes(command, encoding='utf8')

        # check we have a prompt
        data = self.read_until(1, b'>')
        if not data.endswith(b'>'):
            raise PyboardError('could not enter raw repl')

        # write command
        for i in range(0, len(command_bytes), 256):
            self.serial.write(
                command_bytes[i:min(i + 256, len(command_bytes))])
            time.sleep(0.01)
        self.serial.write(b'\x04')

        # check if we could exec command
        data = self.serial.read(2)
        if data != b'OK':
            raise PyboardError('could not exec command')

        # receive data from the serial port
        out = self.receive_serial_data(quiet)
        # Receive data after use '\x03'
        self.receive_serial_data(quiet)

        return out

    def receive_serial_data(self, quiet=True):
        session_data = b''
        data = b''

        # add to lines in the console
        if(not quiet):
            self.data_consumer('\n\n')

        while(b'\x04' not in data):
            data += self.serial.read(1)

            # avoid to print '\x04' char
            if(data.endswith(b'\r\n') and b'\x04' not in data):
                # normalizes end of line for ST
                data = data.replace(b'\r\n', b'\n')
                if(not quiet):
                    self.data_consumer(data)
                session_data += data
                data = b''
        return session_data

    def execfile(self, filename):
        with open(filename, 'rb') as f:
            pyfile = f.read()
        return self.exec_(pyfile, quiet=False)

    def get_time(self):
        t = str(self.eval('pyb.RTC().datetime()'),
                encoding='utf8')[1:-1].split(', ')
        return int(t[4]) * 3600 + int(t[5]) * 60 + int(t[6])
