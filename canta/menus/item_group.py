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
import soya.pudding as pudding
import soya.pudding.ext.meter

from canta.menus.button import MenuButton
from canta.menus.toggle_button import MenuToggle
from canta.menus.menu import ContentMenu

class MenuGroup(ContentMenu):
    def __init__(self, widget_properties, key=""):
        ContentMenu.__init__(self, widget_properties)

        self.widget_properties = widget_properties
        self.group_count = 0
        self.heights = []
        self.toggle_list = []
        self.key = key


    def add_group(self, items):
        # TODO: find out how this works and make it dynamic.
        #if self.group_count == 0:
        #	top = 90
        #elif self.group_count == 1:
        #	top = 90 + 290
        #elif self.group_count == 2:
        #	top = 90 + 290 + 160
        #elif self.group_count == 3:
        #	top = 90 + 290 + 160 + 95

        top = self.box_cont.top

        self.group_cont = pudding.container.VerticalContainer( \
                self, top=top, left=30, width=100, z_index=1)
        self.group_cont.padding = 10
        self.heading_label = pudding.control.SimpleLabel( \
                self.group_cont, top=10, left=15, label=items['heading'], \
                font=self.font_p,
                color=self.color_h)

        bc_top = top + 25
        bc_left = 10
        bc_width = 10 # any number, we ANCHOR_ALL later
        bc_height = 10 # any number, we ANCHOR_ALL later

        box_cont = pudding.container.Container( \
                self, left=bc_left, top=bc_top, \
                width=bc_width, height=bc_height, z_index=-3)
        box_cont.right = 20
        box_cont.bottom = 30
        box_cont.anchors = pudding.ANCHOR_ALL
        box_cont.padding = 5

        box_left = 10
        box_width = self.screen_res_x - 40

        box_height = len(items) * 65
        self.bg_box = pudding.control.Box(box_cont, \
                left=box_left, \
                width=box_width, \
                height=box_height, \
                background_color=self.box_bg_color, \
                border_color=self.box_border_color, \
                z_index=-3)
        self.bg_box.anchors = pudding.ANCHOR_TOP | pudding.ANCHOR_LEFT | pudding.ANCHOR_RIGHT


        for item in items['items']:
            label_string = _('Choose a') + " " + item['info']
            self.info_label = pudding.control.SimpleLabel(self.group_cont, \
                label=label_string, font=self.font_p, left=10, \
                color=self.color_p)
            if item['button_type'] == 'toggle':
                selected_item = item['selected_item']
                self.toggle_list.append(self.group_cont.add_child( \
                    MenuToggle(self.widget_properties, \
                    item['toggle_items'], selected_item, \
                    item['info'])))
            elif item['button_type'] == 'button':
                self.group_cont.add_child(MenuButton(item['label'], \
                    item['function'], item['args'], \
                    self.widget_properties))
        self.group_count += 1


    def add(self, button, align='left'):
        self.nav_cont.add_child(button, pudding.EXPAND_BOTH)
        button.root=self

    def save(self):
        for item in self.toggle_list:
            item.save()

