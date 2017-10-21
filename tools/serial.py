# !/usr/bin/env python
# -*- coding: utf-8 -*-
from ..tools import pyserial
from time import sleep

in_use = []
serial_dict = {}


class Serial:

    def __init__(self, port, baudrate, timeout=1):
        self._serial = pyserial.Serial()
        self._serial.port = port
        self._serial.baudrate = baudrate
        self._serial.timeout = timeout

        self._stop_task = True

    def open(self):
        """Open port

        Opens the port given in the construct.
        _stop_task:     is used to avoid an error when it's closed.
        in_use:         list of port already open
        serial_dict:    dictionary with the serial object
        """
        self._serial.open()
        self._stop_task = False

        # store port used
        port = self._serial.port
        in_use.append(port)
        serial_dict[port] = self

    def receive(self):
        """Receive data

        Receive the data from the selected port

        Returns:
            bytes -- Bytes read from the port
        """
        return self._serial.readline()

    def readable(self):
        """Convert data from byte to string

        Returns in a readable characters/string the byte data received in
        the serial port. It will also replace the end lines to be compatible
        with the Sublime Text end lines (\n)

        Returns:
            str -- readable received data
        """
        data = self.receive()
        data = data.decode('utf-8', 'replace')
        data = data.replace('\r\n', '\n'). replace('\r', '\n')
        return data

    def is_running(self):
        """Check if the port is running

        This method will be set to false before the port is closed, it will
        avoid to get the overlaped error, when the is_open object is used

        Returns:
            bool -- True if the port is running (open) false if not
        """
        return not self._stop_task

    def write(self, data):
        """Write bytedata to the port

        Writes bytedata to the selected serial port

        Arguments:
            data {byte} -- data to send

        Returns:
            int -- Number of bytes written.
        """
        return self._serial.write(data)

    def writable(self, data, line_ending='\r\n'):
        """Write bytes from string

        Writes bytes in the selected port from the readable string sent

        Arguments:
            data {str} -- data to send

        Returns:
            int -- Number of bytes written.
        """
        data += line_ending
        data = data.encode('utf-8', 'replace')

        return self._serial.write(data)

    def close(self):
        """Close serial connection

        Closes the serial connection in the port selected.
        _stop_task will be updated before close the port to avoid the overlaped
        error,
        """
        self._stop_task = True
        self._serial.close()

        port = self._serial.port

        in_use.remove(port)
        del serial_dict[port]
