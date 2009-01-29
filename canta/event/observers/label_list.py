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

class LabelList:
    def __init__(self, widget_properties, debug=0):
    
        self.parent_widget = widget_properties['root_widget']

        self.anchoring = widget_properties['anchoring']
        self.top = widget_properties['pos_size']['top']
        self.left = widget_properties['pos_size']['left']

        self.debug = debug

        self.font_to_sing = widget_properties['font']['lyrics']['to_sing']['obj']
        self.color_to_sing = widget_properties['font']['lyrics']['to_sing']['color']

        self.font_special = widget_properties['font']['lyrics']['special']['obj']
        self.color_special = widget_properties['font']['lyrics']['special']['color']

        self.font_active = widget_properties['font']['lyrics']['active']['obj']
        self.color_active = widget_properties['font']['lyrics']['active']['color']

        self.font_done = widget_properties['font']['lyrics']['done']['obj']
        self.color_done = widget_properties['font']['lyrics']['done']['color']

        self.container = pudding.container.HorizontalContainer(
                self.parent_widget, width=100, \
                left=self.left, \
                top=self.top, z_index=1)

        if self.anchoring == 'bottom':
            self.container.anchors = pudding.ANCHOR_BOTTOM \
                | pudding.ANCHOR_LEFT
        elif self.anchoring == 'top':
            self.container.anchors = pudding.ANCHOR_TOP


    def _delete(self, pos):
        self.container.children[pos].label = ''
        #del self.container.children[pos]


    def _delete_all(self):
        for i in range(len(self.container.children)):
            self._delete(i)
        del self.container.children[0:]
        #self.container.render()
        

    def _next_line(self, song):
        words = song.lines[song.line_nr].segments
        for i in range(len(words)):
            #if i >0 and i < len(words)-1:
            pudding.control.SimpleLabel(self.container,
                    label=words[i].text,
                    font=self.font_to_sing,
                    top=self.top,
                    left=0)

            self.container.children[-1].color = self.color_to_sing

            self.container.on_resize()

            if words[i].special:
                self.container.children[-1].color = self.color_special
                #self.container.children[-1].font = self.font_special

            if words[i].freestyle:
                self.container.children[-1].color = self.color_special
                #self.container.children[-1].font = self.font_special

    def _activate_note(self, pos):
        self.container.children[pos].color = self.color_active
        #self.container.children[pos].font = self.font_active


    def _de_activate_note(self, pos):
        self.container.children[pos].color = self.color_done
        #self.container.children[pos].font = self.font_done


    def _end(self):
        self.container.visible = 0


    def update(self, subject):
        status = subject.data['type']
        if status == 'roundStart':
            pass
        elif status == 'activateNote':
            self._activate_note(subject.data['pos'])
        elif status == 'deActivateNote':
            self._de_activate_note(subject.data['old_pos'])
        elif status == 'nextLine':
            self._delete_all()
            self._next_line(subject.data['song'].lines[subject.data['song'].line_nr].segments)

        elif status == 'end':
            self._end()
        elif self.debug:
            print 'status: ', status


def main():
    pass

if __name__ == '__main__': main()

