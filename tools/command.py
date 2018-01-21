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

import os
import time
import threading
import sublime

from re import findall
from sys import platform
from subprocess import Popen, PIPE
from functools import partial
from collections import deque

from ..tools import message, paths
from ..tools.thread_progress import ThreadProgress

_COMMAND_QUEUE = deque()
_BUSY = False


class AsyncProcess(object):

    def __init__(self, cmd, listener):
        self.listener = listener
        self.killed = False
        self.start_time = time.time()

        self.proc = Popen(
            cmd,
            stdout=PIPE,
            stderr=PIPE,
            stdin=PIPE,
            shell=True)

        if(self.proc.stdout):
            th = threading.Thread(target=self.read_stdout)
            th.start()

            ThreadProgress(th, '', '')

        if(self.proc.stderr):
            threading.Thread(target=self.read_stderr).start()

    def kill(self):
        """Kill process

        kill the encapsulated subprocess.Popen
        """
        if(not self.killed):
            self.killed = True
            if(platform == 'win32'):
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                subprocess.Popen("taskkill /PID " + str(self.proc.pid),
                                 startupinfo=startupinfo)
            else:
                self.proc.terminate()
            self.listener = None

    def poll(self):
        return self.proc.poll() is None

    def exit_code(self):
        """
        return the exit code
        """
        return self.proc.poll()

    def read_stdout(self):
        """Read stdout output

        Reads the stdout outputs when the data is available
        and send it to the listener to be printed
        """
        while True:
            data = os.read(self.proc.stdout.fileno(), 2 ** 15)

            if(len(data) > 0):
                if(self.listener):
                    self.listener.on_data(data)
            else:
                self.proc.stdout.close()
                if(self.listener):
                    self.listener.on_finished(self)
                break

    def read_stderr(self):
        """Read stderr output

        Reads the stderr outputs when the data is available
        and send it to the listener to be printed
        """
        while True:
            data = os.read(self.proc.stderr.fileno(), 2 ** 15)

            if len(data) > 0:
                if self.listener:
                    self.listener.on_data(data)
            else:
                self.proc.stderr.close()
                break


class Command:
    txt = None

    def run(self, cmd, port=None, working_dir="", kill=False, word_wrap=True):
        self.window = sublime.active_window()

        global _COMMAND_QUEUE
        global _BUSY

        # kill the process
        if(kill):
            if(self.proc):
                self.proc.kill()
                self.proc = None
            return

        if(_BUSY):
            _COMMAND_QUEUE.append(cmd)
            return

        self.txt = message.open(port)

        self.encoding = 'utf-8'
        self.quiet = False
        self.proc = None

        cmd = prepare_command(cmd)

        if not self.quiet:
            if cmd:
                cmd_string = findall(r'\"(.+?)\"', cmd)
                cmd_string = os.path.normpath(cmd_string[0])
                cmd_string = os.path.basename(cmd_string)
                lindex = cmd.rfind('"')
                cmd_string += cmd[lindex:].replace('"', '')

                self.txt.print("\n\nRunning {}\n\n" .format(cmd_string))

        if working_dir != "":
            os.chdir(working_dir)

        try:
            _BUSY = True
            self.proc = AsyncProcess(cmd, self)
        except Exception as e:
            pass

    def on_data(self, data):
        try:
            characters = data.decode(self.encoding)
        except:
            characters = "[Decode error - output not " + self.encoding + "]\n"

        # Normalize newlines, Sublime Text always uses a single \n separator
        # in memory.
        characters = characters.replace('\r\n', '\n').replace('\r', '\n')
        self.txt.print(characters)

    def finish(self, proc):
        elapsed = time.time() - proc.start_time
        exit_code = proc.exit_code()

        if(exit_code == 0 or exit_code is None):
            txt = "\n[Finished in {0:.1f}s]".format(elapsed)
            self.txt.print(txt)
        else:
            txt = "\n[Finished in {0:.1f}s with exit code {1}]\n".format(
                elapsed, exit_code)
            self.txt.print(txt)

        if(proc != self.proc):
            return

        if(exit_code == 0):
            sublime.status_message("Build finished")
        else:
            sublime.status_message("Build finished with errors")

        # run next command in the deque
        run_next()

    def on_finished(self, proc):
        sublime.set_timeout(partial(self.finish, proc), 0)


def run_next():
    global _COMMAND_QUEUE
    global _BUSY

    _BUSY = False

    if(len(_COMMAND_QUEUE)):
        Command().run(_COMMAND_QUEUE.popleft())


def prepare_command(options):
    esptool = paths.esptool_file()

    cmd = ['python', '"' + esptool + '"']
    cmd.extend(options)
    cmd.append("2>&1")
    cmd = " ".join(cmd)

    return cmd
