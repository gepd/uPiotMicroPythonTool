# !/usr/bin/env python
# -*- coding: utf-8 -*-
from .commands import *
from sublime_plugin import EventListener
from .tools import serial


class uPiotListener(EventListener):

    def on_close(self, view):
        port = serial.selected_port()
        if(port in serial.in_use):
            serial.serial_dict[port].close()
