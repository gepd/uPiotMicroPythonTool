# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sublime
from .. import tools

view_group = None
viewer_name = '$ Micropython Viewer'


class Message:
    output = None

    def __init__(self):
        self.recover_output()

    def create_panel(self, text=None, direction='down'):
        """output panel

        Creates a output panel to print messages in file window
        """
        global viewer_name

        window, view = self.get_message_winview()

        if(not view):
            window = sublime.active_window()

            options = {'direction': direction, 'give_focus': True}
            window.run_command('create_pane', options)

            self.output = window.new_file()
            self.output.set_name(viewer_name)
            self.output.run_command('toggle_setting', {'setting': 'word_wrap'})
            self.output.set_scratch(True)

            if(text):
                self.print(text)
        else:
            self.recover_output()

    def recover_output(self):
        window, view = self.get_message_winview()
        if(view):
            self.output = view

    @staticmethod
    def get_message_winview():
        """Window and view from message viewer

        Gets the window and view sublime text object from the message
        viewer.

        Returns:
            obj, obj -- window, view
        """
        return tools.find_view(viewer_name)

    def is_created(self):
        """Check viewer panel creation

        Checks if the message viewer windows was already created

        Returns:
            bool -- True if was created, False if not
        """
        window, view = self.get_message_winview()
        return bool(view)

    def print(self, text):
        """print message

        Prints the given message in the output panel in a separated
        thread to avoid block the UI

        Arguments:
            text {str} -- message to print
        """

        def block_print():
            self.output.set_read_only(False)
            self.output.run_command('append', {'characters': text})
            self.output.set_read_only(True)
        sublime.set_timeout_async(block_print, 0)

    def check_message_group():
        """Get message view group

        Gets the group number of the message view before close it
        """
        global view_group

        window = sublime.active_window()
        view = window.active_view()

        view_group = None

        if(view and viewer_name in view.name()):
            view_group = window.active_group()

    @staticmethod
    def close_panel():
        """close output panel

        Closes the output panel if it's open.
        """

        global view_group

        if(view_group):
            window = sublime.active_window()
            window.focus_group(view_group)
            window.run_command('destroy_pane', {'direction': 'self'})
