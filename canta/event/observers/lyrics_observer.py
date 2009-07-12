#! /usr/bin/python -O
# -*- coding: utf-8 -*-
#
#    CANTA - A free entertaining educational software for singing
#    Copyright (C) 2007  S. Huchler, A. Kattner, F. Lopez
#    Copyright (C) 2008  S. Huchler
#    Copyright (C) 2009  S. Huchler
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
from canta.event.observers.label_list import LabelList

class LyricsObserver(pudding.container.Container):

    def __init__(self, widget_properties, line_diff=0):

        parent = widget_properties['root_widget']
        self.line_diff = line_diff
        screen_res_x = int(widget_properties['config']['screen']['resolution'].split('x')[0])
        screen_res_y = int(widget_properties['config']['screen']['resolution'].split('x')[1])

        bc_top = widget_properties['pos_size']['top']
        bc_left = int (0.02 * screen_res_x)
        bc_width = screen_res_x * 0.9 # any number, we ANCHOR_ALL later
        bc_height = screen_res_y * 0.07
        pudding.container.Container.__init__( \
                self, parent=parent, left=bc_left, top=bc_top,\
                width=bc_width, height=bc_height)

        box_border_color = widget_properties['box']['border']['color']
        box_bg_color = widget_properties['box']['background']['color']
        box_left = self.left
        box_width = self.width
        box_height = self.height
        bg_box = pudding.control.Box(self, \
                left=box_left, \
                width=box_width, \
                height=box_height, \
                background_color=box_bg_color, \
                border_color=box_border_color, \
                z_index=-3)
        bg_box.anchors = pudding.ANCHOR_BOTTOM | pudding.ANCHOR_LEFT \
                | pudding.ANCHOR_RIGHT
        self.label_list = LabelList(bg_box, widget_properties)


    def update(self, subject):
        status = subject.data['type']
        if status == 'nextLine':
            song = subject.data['song']
            self.label_list._delete_all()
            line_nr = song.line_nr + self.line_diff
            if 0 <= line_nr < len(song.lines):
                self.label_list._show_line(song.lines[line_nr].segments)
        elif status == 'activateNote':
            if self.line_diff == 0:
                self.label_list._activate_note(subject.data['pos'])
        elif status == 'deActivateNote':
            if self.line_diff == 0:
                self.label_list._de_activate_note(subject.data['old_pos'])
        elif status == 'end':
            self.visible = 0



def main():
    pass


if __name__ == '__main__': main()

