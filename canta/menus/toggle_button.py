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

class MenuToggle(pudding.control.Button):
    """TODO.
    """
    # TODO: Inherit from own button, because its almost the same...
    def __init__(self, widget_properties, toggle_list, selected_item, key=''):

        self.font_on = widget_properties['font']['button']['on_focus']['obj']
        self.font_off = widget_properties['font']['button']['off_focus']['obj']

        self.font_color_on = widget_properties['font']['button']['on_focus']['color']
        self.font_color_off = widget_properties['font']['button']['off_focus']['color']

        self.bg_color_on = widget_properties['button']['background']['on_focus']['color']
        self.bg_color_off = widget_properties['button']['background']['off_focus']['color']

        self.border_color_on = widget_properties['button']['border']['on_focus']['color']
        self.border_color_off = widget_properties['button']['border']['off_focus']['color']

        self.config = widget_properties['config']

        pudding.control.Button.__init__(self, \
            width = int(widget_properties['config']['screen']['resolution'].split('x')[0]) / 6)

        self.key=key
        self.border_color = self.border_color_off
        self.background_color = self.bg_color_off
        self.child.font = self.font_off
        self.child.color = self.font_color_off

        self.toggle_list = toggle_list

        #
        if type(selected_item) == int:
            self.selected_item = selected_item
        else:
            self.selected_item = self.toggle_list.index(selected_item)

        self.active_item = self.toggle_list[self.selected_item]
        self.label = self.active_item


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
        if self.selected_item + 1 > len(self.toggle_list) - 1:
            self.selected_item = 0
        else:
            self.selected_item = self.selected_item + 1

        self.active_item = self.toggle_list[self.selected_item]
        self.label = self.active_item


    def get_active_item():
        return self.active_item

    def save(self):
        self.config[self._parent._parent.key][self.key] = self.active_item

