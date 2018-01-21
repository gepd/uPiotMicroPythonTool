# This file is part of the uPiot project, https://github.com/gepd/upiot/
#
# MIT License
#
# Copyright (c) 2017 GEPD
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sublime
from sublime_plugin import WindowCommand
from threading import Thread

from ..tools import sampy_manager
from ..tools.serial import selected_port
from ..tools.thread_progress import ThreadProgress


class upiotPutCurrentFileCommand(WindowCommand):

    def run(self):
        port = selected_port(request_port=True)
        if(not port):
            return

        file = self.window.active_view().file_name()

        th = Thread(target=sampy_manager.put_file, args=(file,))
        th.start()
        ThreadProgress(th, '', '')
