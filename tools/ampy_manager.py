import sublime

from os import path, mkdir
from ..tools import check_sidebar_folder
from ..tools import message
from ..tools.sampy import Sampy
from ..tools import serial
from ..tools.ampy import files, pyboard

txt = None
run_serial = None


def start_sampy():
    """
    Opens the sampy connection in the selected port. If already is a serial
    connection running it will look into it and close it.

    Returns:
        Sampy -- Sampy object
    """
    global txt
    global run_serial

    port = serial.selected_port()

    # close the current connection in open port
    if(port in serial.in_use):
        run_serial = serial.serial_dict[port]
        run_serial.close()

    # message printer
    if(message.session):
        txt = message.session
    else:
        if(message.Message().recover_panel(port)):
            txt = message.session

    return Sampy(port)


def finished_action():
    """
    This function will be called after an action is finished, and will
    re-open the serial connection if was open.
    """
    global run_serial

    if(run_serial):
        run_serial.open()
        run_serial.keep_listen(txt.print)


def run_file(filepath):
    """Run file in device

    Runs the given file in the selected device.

    Arguments:
        filepath {str} -- file path
    """
    global txt

    sampy = start_sampy()

    # print command name
    file = path.basename(filepath)
    txt.print('\n\n>> Run {}'.format(file))

    try:
        output = sampy.run(filepath)
        output = output.replace('\r\n', '\n').rstrip()
    except pyboard.PyboardError as e:
        print(str(e))
        output = ""
        # get error
        output = str(e)
        # converted in tuple and extract the 'Traceback' error
        output = str(eval(output)[2])[2:-1]
        # replace \r\n strings
        output = output.replace('\\r\\n', '\n')
        # replace scape slash
        output = output.replace('\\\'', '\'')

    if(message):
        txt.print('\n\n' + output)
    else:
        print(output)

    sampy.close()

    finished_action()


def list_files():

    sampy = start_sampy()

    txt.print('\n\n>> sampy ls\n')

    for filename in sampy.ls():
        txt.print('\n' + filename)

    sampy.close()

    finished_action()


def get_file(filename):
    sampy = start_sampy()

    txt.print('\n\n>> get {0}'.format(filename))
    output = sampy.get(filename)
    output = output.replace('\r\n', '\n').replace('\r', '\n')

    txt.print('\n\n' + output)

    sampy.close()

    finished_action()


def get_files(destination):
    """Get files from devices

    Gets all the files in the device and stored in the selected destination
    path.
    """
    sampy = start_sampy()

    destination = path.normpath(destination)

    txt.print('\n\n>> get from device to {0}'.format(destination))

    for filename in sampy.ls():
        filepath = path.normpath(path.join(destination, filename))
        if(filename.endswith('/')):
            if(not path.exists(filepath)):
                mkdir(filepath)
        else:
            with open(filepath, 'w') as file:
                file.write(sampy.get(filename))

    txt.print('\n\ndone')

    sampy.close()

    finished_action()

    if(check_sidebar_folder(destination)):
        return

    caption = "files retrieved, would you like to" \
        "add the folder to your current proyect?"
    answer = sublime.yes_no_cancel_dialog(caption, "Add", "Append")

    if(answer == sublime.DIALOG_CANCEL):
        return

    if(answer == sublime.DIALOG_YES):
        append = False
    elif(answer == sublime.DIALOG_NO):
        append = True

    options = {'folder': destination, 'append': append}
    sublime.active_window().run_command('upiot_add_project', options)


def put_file(filepath):
    """Put given file in device

    Puts the given in the selected device

    Arguments:
        filepath {str} -- path of the file to put
    """
    sampy = start_sampy()

    file = path.basename(filepath)
    txt.print('\n\n>> putting {0}'.format(file))

    try:
        sampy.put(path.normpath(filepath))
        txt.print('\n\ndone')
    except:
        pass

    sampy.close()

    finished_action()


def remove_file(filepath):
    """Remove file in device

    Removes the given file in the selected device

    Arguments:
        filepath {str} -- file to remove
    """
    sampy = start_sampy()

    file = path.basename(filepath)
    txt.print('\n\n>> remove {0}'.format(file))

    try:
        sampy.rm(filepath)
        txt.print('\n\ndone')
    except:
        txt.print("\n\nerror removing file")

    sampy.close()

    finished_action()


def make_folder(folder_name):
    """Create folder

    Makes a folder in the selected device

    Arguments:
        folder_name {str} -- folder name
    """
    sampy = start_sampy()

    txt.print('\n\n>> creating {0}'.format(folder_name))

    try:
        sampy.mkdir(folder_name)
        txt.print('\n\ndone')
    except files.DirectoryExistsError:
        txt.print("\n\nFolder already exists")

    sampy.close()

    finished_action()


def remove_folder(folder_name):
    """Remove folder from device

    Removes the given folder in the selected device

    Arguments:
        folder_name {str} -- folder to remvoe
    """
    sampy = start_sampy()

    txt.print('\n\n>> Removing {0}'.format(folder_name))

    try:
        sampy.rmdir(folder_name)
        txt.print('\n\ndone')
    except RuntimeError as e:
        if('No such directory' in str(e)):
            txt.print("\n\nFolder no found")

    sampy.close()

    finished_action()
