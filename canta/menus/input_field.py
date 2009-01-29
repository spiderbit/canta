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

import soya.pudding as pudding
from canta.event.keyboard_event import KeyboardEvent
import soya.sdlconst
import time

class InputField(soya.Body):
    """TODO.
    """
    # TODO: Inherit from own button, because its almost the same...
    def __init__(self, widget_properties, text):

        self.font_on = widget_properties['font']['button']['on_focus']['obj']
        self.font_off = widget_properties['font']['button']['off_focus']['obj']

        self.font_color_on = widget_properties['font']['button']['on_focus']['color']
        self.font_color_off = widget_properties['font']['button']['off_focus']['color']

        self.bg_color_on = widget_properties['button']['background']['on_focus']['color']
        self.bg_color_off = widget_properties['button']['background']['off_focus']['color']

        self.border_color_on = widget_properties['button']['border']['on_focus']['color']
        self.border_color_off = widget_properties['button']['border']['off_focus']['color']

        self.parent_world = widget_properties['root_world']
        self.parent_widget = widget_properties['root_widget']

        self.label = pudding.control.Input(self.parent_widget,text, top = 0, 
            left = 0, width = 100, height = 50)
        
        self.done = False

        self.post_method = None

        self.border_color = self.border_color_off
        self.background_color = self.bg_color_off
        self.label.child.font = self.font_off
        self.label.child.color = self.font_color_off

        self.shift = False
        self.ctrl = False
        self.alt = False

    def begin_round(self):
        soya.Body.begin_round(self)
        # go through the events:
        for event in soya.process_event():
            
            # key pressed:
            if event[0] == soya.sdlconst.KEYDOWN:
#				for x in range(len(event)):
#					print "event[",x,"]: ", event[x]
                if event[1] == soya.sdlconst.K_ESCAPE:
                    if self.post_method is not None:
                        self.post_method()
                elif event[1] == soya.sdlconst.K_KP_ENTER \
                        or event[1] == soya.sdlconst.SYSWMEVENT:
                    self.done = True
                    if self.post_method is not None:
                        self.post_method()
                elif event[1] == soya.sdlconst.K_RSHIFT \
                        or event[1] == soya.sdlconst.K_LSHIFT:
                    self.shift = True
                elif event[1] == soya.sdlconst.K_RALT \
                        or event[1] == soya.sdlconst.K_LALT:
                    self.alt = True
                elif event[1] == soya.sdlconst.K_RCTRL \
                        or event[1] == soya.sdlconst.K_LCTRL:
                    self.ctrl = True
                elif event[3] == soya.sdlconst.K_BACKSPACE:
                    self.label.value = self.label.value[0:-1]
                elif event[3] == soya.sdlconst.K_UNKNOWN:
                    pass
                    
                elif event[3] < 256:
                    key = unichr(event[3])
                    #if len(event) > 2:
                    #	print event[2]
                    if self.shift:
                        key = key.upper()
                    self.label.value = self.label.value + key
                #else:
                    #for x in range(len(event)):
                        #print "event[",x,"]: ", event[x]

            elif event[0] == soya.sdlconst.KEYUP:
                if event[1] == soya.sdlconst.K_RSHIFT \
                        or event[1] == soya.sdlconst.K_LSHIFT:
                    self.shift = False
                elif event[1] == soya.sdlconst.K_RALT \
                        or event[1] == soya.sdlconst.K_LALT:
                    self.alt = False
                elif event[1] == soya.sdlconst.K_RCTRL \
                        or event[1] == soya.sdlconst.K_LCTRL:
                    self.ctrl = False
                #else:
                    #print event[1]

            #else:
                #print event[0]


