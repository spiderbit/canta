#! /usr/bin/python -O
# -*- coding: utf-8 -*-
#
#    CANTA - A free entertaining educational software for singing
#    Copyright (C) 2007  S. Huchler, A. Kattner, F. Lopez
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
import os

import soya
import time
import soya.pudding as pudding


class KeyboardEvent(soya.Body):
    def __init__(self, widget_properties = None, theme_mgr=None):
        self.parent_widget = widget_properties['root_widget']
        self.shift = False
        self.ctrl = False
        self.alt = False
        self.observed_events = []


    def add_connection(self, type, action,  args = None):
        self.observed_events.append({'type': type, 'action': action, 'args': args })


    def reset(self):
        self.observed_events=[]


    def begin_round(self):
        soya.Body.begin_round(self)
        # go through the events:
        for event in soya.process_event():
            # key pressed:
            if event[0] == soya.sdlconst.KEYDOWN:
                # [ARROW UP] - no action:
                for observed_event in self.observed_events:
                    if event[1] == observed_event['type']:
                        if observed_event['args'] is not None:
                            observed_event['action'](observed_event['args'])
                        else:
                            observed_event['action']()
                        break
                else:
                    if event[1] == soya.sdlconst.K_RSHIFT \
                            or event[1] == soya.sdlconst.K_LSHIFT:
                        self.shift = True
                    elif event[1] == soya.sdlconst.K_RCTRL \
                            or event[1] == soya.sdlconst.K_LCTRL:
                        self.ctrl = True
                    elif event[1] == soya.sdlconst.K_RALT \
                            or event[1] == soya.sdlconst.K_LALT:
                        self.alt = True

            elif event[0] == soya.sdlconst.KEYUP:
                if event[1] == soya.sdlconst.K_RSHIFT \
                        or event[1] == soya.sdlconst.K_LSHIFT:
                    self.shift = False
                elif event[1] == soya.sdlconst.K_RCTRL \
                        or event[1] == soya.sdlconst.K_LCTRL:
                    self.ctrl = False
                elif event[1] == soya.sdlconst.K_RALT \
                        or event[1] == soya.sdlconst.K_LALT:
                    self.alt = False

