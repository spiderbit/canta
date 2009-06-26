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
import time
import soya
import soya.pudding as pudding

class TimeLabel:
    """Draw a label that displays the song play time.
    """
    def __init__(self, widget_properties, debug=0):

        self.debug = debug
        self.parent_widget = widget_properties['root_widget']
        self.font_p = widget_properties['font']['p']['obj']
        self.color_p = widget_properties['font']['p']['color']
        self.top = 10
        self.left = 20
        height = 200
        self.z_index = 4

        self.time_word = _(u'Time: ')
        time_pos = '00:00'

        self.container = pudding.container.HorizontalContainer( \
                self.parent_widget, height=height, \
                left=self.left, top=self.top)
        self.container.anchors = pudding.ANCHOR_RIGHT \
                 | pudding.ANCHOR_TOP | pudding.ANCHOR_LEFT
        self.container.add_child(pudding.control.SimpleLabel(
                    label=self.time_word + time_pos,
                    font=self.font_p,
                    color=self.color_p))
        self.container.on_resize()


    def _end(self):
        del self.container.children[0:]


    def _set_time(self, player):
        pos = int(player.get_pos())
        duration = int(player.get_duration())
        time_pos = time.strftime("%M:%S",time.gmtime(pos))
        time_duration = time.strftime("%M:%S",time.gmtime(duration))
        self.container.children[0].label = self.time_word + time_pos + ' / ' + time_duration

    def update(self, subject):
        status = subject.data['type']
        if status == 'roundStart':
            self._set_time(subject.data['player'])
        elif status == 'end':
            self._end()
        elif self.debug:
            print 'status: ', status



def main():
    pass

if __name__ == '__main__': main()

