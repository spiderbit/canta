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

class MenuButton(pudding.control.Button):
    def __init__(self, label='none', function=None, args=None, \
            widget_properties=[], pos_size=None, target = None):

        self.function = function
        self.target = target
        self.root = None
        self.args = args
        self.visible = 1

        self.font_on = widget_properties['font']['button']['on_focus']['obj']
        self.font_off = widget_properties['font']['button']['off_focus']['obj']

        self.font_color_on = widget_properties['font']['button']['on_focus']['color']
        self.font_color_off = widget_properties['font']['button']['off_focus']['color']

        self.bg_color_on = widget_properties['button']['background']['on_focus']['color']
        self.bg_color_off = widget_properties['button']['background']['off_focus']['color']

        self.border_color_on = widget_properties['button']['border']['on_focus']['color']
        self.border_color_off = widget_properties['button']['border']['off_focus']['color']


        # When I use "if blah_thing is not None" here, everything explodes.
        if pos_size:
            self.width = pos_size['width']
            self.height = pos_size['height']
            self.top = pos_size['top']
            self.left = pos_size['left']

            pudding.control.Button.__init__(
                    self, label=label, width=self.width, \
                    height=self.height, top=self.top, \
                    left=self.left, z_index=1)
        else:
            pudding.control.Button.__init__(self, label=label, z_index=1)

        self.border_color = self.border_color_off
        self.background_color = self.bg_color_off
        self.child.font = self.font_off
        self.child.color = self.font_color_off
        #self.old_label = self.child.label


    def on_focus(self):
        self.border_color = self.border_color_on
        self.background_color = self.bg_color_on
        #self.child.font = self.font_on
        self.child.color = self.font_color_on
        #self.child.label = '+'+self.old_label+'+'


    def on_loose_focus(self):
        self.border_color = self.border_color_off
        self.background_color = self.bg_color_off
        #self.child.font = self.font_off
        self.child.color = self.font_color_off
        #self.child.label = self.old_label


    def on_mouse_up(self, button, x, y):
        if self.function != None:
            if self.args == None:
                self.function()
            else:
                self.function(self.args)
        if self.target != None:
            self.root.hide()
            self.target.show()
        return True

