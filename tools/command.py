# !/usr/bin/env python
# -*- coding: utf-8 -*-

from ..tools import paths
import subprocess


def run_command(command, cwd=None):

    command = prepare_command(command)
    process = subprocess.Popen(command, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, cwd=cwd,
                               universal_newlines=True, shell=True)

    while True:
        output = process.stdout.readline()
        # exit when there is nothing to show
        if output == '' and process.poll() is not None:
            break

        if output:
            print(output)


def prepare_command(options):
    esptool = paths.esptool_file()

    cmd = ['python', '"' + esptool + '"']
    cmd.extend(options)
    cmd.append("2>&1")
    cmd = " ".join(cmd)

    return cmd
