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

import os
import soya
import soya.pudding as pudding

class LyricsBgBox:
    """ Draw a background box for the lyrics.
    """
    def __init__(self, widget_properties, debug=0):
    
        parent_widget = widget_properties['root_widget']

        screen_res_x = widget_properties['config']['screen'].as_int('resolution_x')
        screen_res_y = widget_properties['config']['screen'].as_int('resolution_y')

        box_border_color = widget_properties['box']['border']['color']
        box_bg_color = widget_properties['box']['background']['color']

        bc_top = screen_res_y / 1.1 - 20
        bc_left = 10
        bc_width = 10 # any number, we ANCHOR_ALL later
        bc_height = screen_res_y
        self.box_cont = pudding.container.Container( \
                parent_widget, left=bc_left, top=bc_top,\
                width=bc_width, height=bc_height)
        self.box_cont.right = 20
        self.box_cont.bottom = 30
        self.box_cont.anchors = pudding.ANCHOR_ALL
        self.box_cont.padding = 5

        box_left = 10
        box_width = screen_res_x - 40
        box_height = screen_res_y - bc_top - 25
        bg_box = pudding.control.Box(self.box_cont, \
                left=box_left, \
                width=box_width, \
                height=box_height, \
                background_color=box_bg_color, \
                border_color=box_border_color, \
                z_index=-3)
        bg_box.anchors = pudding.ANCHOR_BOTTOM | pudding.ANCHOR_LEFT \
                | pudding.ANCHOR_RIGHT

        parent_widget.on_resize()


    def _end(self):
        self.box_cont.visible = 0


    def update(self, subject):
        status = subject.data['type']
        if status == 'end':
            self._end()


def main():
    pass

if __name__ == '__main__': main()

