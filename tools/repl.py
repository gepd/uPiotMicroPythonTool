import time
import sublime

from . import serial
from threading import Thread


class Repl:

    def __init__(self, serial, data_consumer):
        self.data_consumer = data_consumer
        self.serial = serial

    def enter_raw(self):
        """Enters in raw repl mode

        Enters in the raw repl, to do it, it first checks send two cancel
        commands and then reads the data in the serial port. It's made to
        avoid run flushIn(). If there is not data after 450ms, the raw REPL
        command will be send once, and then, the loop will be waiting for the
        "raw REPL; CTRL-B to exit" text. it will confirm the raw REPL mode.
        """
        output_start = getMillTime()
        current_time = getMillTime()
        cmd_repl = False
        data = b''

        # ctrl-C ctrl-C
        self.serial.write(b'\r\x03\x03')

        while(True):
            current_time = getMillTime()

            # if there no data for 450ms send raw repl command
            if(current_time - output_start > 450 and not cmd_repl):
                self.exit_raw()
                # ctrl-A raw REPL
                self.serial.write(b'\r\x01')
                cmd_repl = True

            if(self.serial.inWaiting() > 0):
                # reset counter
                output_start = getMillTime()
                # read
                r = self.serial.readline()
                if(r.endswith(b'raw REPL; CTRL-B to exit\r\n')):
                    break

                # if end of file char detected break loop
                if(r.endswith(b'\x04')):
                    break

    def exit_raw(self):
        """Close raw repl mode

        Sends the \x02 command to enter in the friendly REPL mode
        """
        # ctrl-B: enter friendly REPL
        self.serial.write(b'\r\x02')

    def receive_serial_data(self, quiet=True):
        """Read serial data comming

        Reads the serial data comming throug the serial port.
        The data_consumer method is used to print the data in the
        console in realtime. When the loop receives the \x04 char
        it will end and the session data will be returned

        Keyword Arguments:
            quiet {bool} -- When it's false no data is printed in the console
                        (default: {True})

        Returns:
            byte str -- all data received while the loop was running
        """
        data = b''
        session_data = b''

        # add to lines in the console
        if(not quiet):
            self.data_consumer('\n\n')

        while(True):

            if(self.serial.inWaiting() > 0):
                data += self.serial.read(1)

                if(data.endswith(b'\x04')):
                    break

                if(data.endswith(b'\r\n')):
                    # normalizes end of line for ST
                    data = data.replace(b'\r\r\n', b'\n')
                    data = data.replace(b'\r\n', b'\n')

                    session_data += data

                    if(not quiet):
                        self.data_consumer(data)
                        data = b''

        return session_data

    def read_until(self, min_bytes, ending, timeout=10, quiet=True):
        """Read until givin string

        Reads until find the given string otherwise, wait until the
        timeout is met.

        Arguments:
            min_bytes {int} -- minimum bytes to read each time in serial.read
            ending {str} -- char o string to search

        Keyword Arguments:
            timeout {number} -- time to stop the execution if
                                there not match (default: {10})
            quiet {bool} -- When it's false displays the output in the
                                data_consumer function (default: {True})

        Returns:
            [str] -- All data received by the serial while the method runs
        """
        data = self.serial.read(1)

        if(not quiet):
            self.data_consumer(data)

        time_count = 0

        while True:
            if(data.endswith(ending)):
                break
            elif(self.serial.inWaiting() > 0):
                new_data = self.serial.read(1)
                data += new_data
                if(not quiet):
                    self.data_consumer(new_data)
                time_count = 0
            else:
                time_count += 1
                if(timeout is not None and time_count >= 100 * timeout):
                    break
                time.sleep(0.01)
        return data

    def exec_(self, command, quiet=True):
        """Executes a command

        Convert the command in bytes and execute it in the
        remote device, after that the output will be printed
        and/or received

        Arguments:
            command {str/byte} -- command to run in the device

        Keyword Arguments:
            quiet {bool} -- When it's false, no data is printed in the console
                            (default: {True})

        Returns:
            byte str -- data received after sends the commands

        Raises:
            ReplError -- error when command confirmation is not get
        """
        if isinstance(command, bytes):
            cmd_bytes = command
        else:
            cmd_bytes = bytes(command, encoding='utf8')

        # check prompt
        data = self.read_until(1, b'>')
        if(not data.endswith(b'>')):
            raise PyboardError('could not enter raw repl')

        # write command
        for i in range(0, len(cmd_bytes), 256):
            self.serial.write(cmd_bytes[i:min(i + 256, len(cmd_bytes))])
            time.sleep(0.01)
        self.serial.write(b'\x04')

        # check if we could exec command
        data = self.serial.read(2)
        if b'OK' not in data:
            raise ReplError('could not exec command')

        # receive data from the serial port
        out = self.receive_serial_data(quiet)

        return out

    def execfile(self, filename):
        """Execute file

        Opens and return the conten of a local file

        Arguments:
            filename {str} -- path of the file to open

        Returns:
            bytes -- file content
        """

        try:
            with open(filename, 'rb') as f:
                pyfile = f.read()
        except OSError as e:
            pyfile = filename

        return self.exec_(pyfile, quiet=False)


class ReplError(BaseException):
    pass


def getMillTime():
    """Current time

    Current time in milliseconds

    Returns:
        int -- current time
    """
    return int(round(time.time() * 1000))
