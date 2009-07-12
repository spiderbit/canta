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

class Menu(pudding.container.Container):
    def __init__(self, widget_properties):
        self.widget_properties = widget_properties
        parent = widget_properties['root_widget']
        pudding.container.Container.__init__(self, \
            parent = parent, width=parent.width, \
                height=parent.height, \
                top=0, left=0)
        self.visible = 0
        self.parent_world = widget_properties['root_world']
        self.screen_res_x = int(widget_properties['config']['screen']['resolution'].split('x')[0])
        self.screen_res_y = int(widget_properties['config']['screen']['resolution'].split('x')[1])
        self.font_p = widget_properties['font']['p']['obj']
        self.color_p = widget_properties['font']['p']['color']
        self.font_h = widget_properties['font']['h1']['obj']
        self.color_h = widget_properties['font']['h1']['color']
        self.box_border_color = widget_properties['box']['border']['color']
        self.box_bg_color = widget_properties['box']['background']['color']
        self.hc_height = self.screen_res_y / 20

        vc_top = self.screen_res_y / 3
        vc_left = 40
        self.v_cont = pudding.container.VerticalContainer(
                self, left=vc_left, top=vc_top, z_index = 1)
        self.v_cont.anchors = pudding.ANCHOR_ALL
        self.v_cont.padding = 10

        # The container for global navigation:
        self.nc_top = self.hc_height + 10
        self.nc_left = 20
        self.nc_height = self.screen_res_y / 20
        self.nav_cont = pudding.container.HorizontalContainer( \
                self, left=self.nc_left, top=self.nc_top, \
                height=self.nc_height)
        self.nav_cont.right = 30
        self.nav_cont.anchors = pudding.ANCHOR_RIGHT \
                     | pudding.ANCHOR_TOP | \
                    pudding.ANCHOR_LEFT
        self.nav_cont.padding = 5

        # The container for the heading:
        self.heading_cont = pudding.container.HorizontalContainer( \
            self, left=20, top=10, \
            height=self.hc_height)
        self.heading_cont.right = 15
        self.heading_cont.anchors =  pudding.ANCHOR_RIGHT \
                 | pudding.ANCHOR_TOP | pudding.ANCHOR_LEFT
        self.heading_cont.padding = 5


    def add(self, button, cont_type='vert'):
        if cont_type == 'horiz':
            self.nav_cont.add_child(button, pudding.EXPAND_BOTH)
        elif cont_type == 'vert':
            self.add_child(button)
        else:
            self.v_cont.add_child(button, pudding.CENTER_VERT)

        button.root=self


    def show(self):
        self.visible=1

    def hide(self):
        self.visible=0


    def set_heading(self, text):
            self.heading_cont.add_child(pudding.control.SimpleLabel( \
                label=text, font=self.font_h, \
                color=self.color_h), pudding.EXPAND_BOTH)


class ContentMenu(Menu):
    def __init__(self, widget_properties):
        Menu.__init__(self, widget_properties)

        # The container for the background box:
        bc_top = self.nc_top + 10 + self.nc_height
        bc_left = 10
        bc_width = 10 # any number, we ANCHOR_ALL later
        bc_height = self.screen_res_y

        self.box_cont = pudding.container.Container( \
                self, left=bc_left, top=bc_top,\
                width=bc_width, height=bc_height)
        self.box_cont.right = 20
        self.box_cont.bottom = 30
        self.box_cont.anchors = pudding.ANCHOR_ALL
        self.box_cont.padding = 5

        box_left = 10
        box_width = self.screen_res_x - 40
        box_height = self.screen_res_y - bc_top - 25

        self.bg_box = pudding.control.Box(self.box_cont, \
                left=box_left, \
                width=box_width, \
                height=box_height, \
                background_color=self.box_bg_color, \
                border_color=self.box_border_color, \
                z_index=-3)
        self.bg_box.anchors = pudding.ANCHOR_ALL

