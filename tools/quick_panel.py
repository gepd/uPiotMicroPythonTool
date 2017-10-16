#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sublime

quick_panel_active = False
quick_panel_id = 0


def quick_panel(items, callback, window=False, flags=0, index=0):
    if(not flags):
        flags = sublime.KEEP_OPEN_ON_FOCUS_LOST
    window = sublime.active_window()
    window.show_quick_panel(items, callback, flags, index)
