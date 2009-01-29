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

class DebugWidget:
    def __init__(self, parent_widget=None, font=None, top=0, left=0, \
            z_index=1, debug=0):
    
        self.parent_widget = parent_widget
        self.font = font
        self.top = top
        self.left = left
        self.z_index = z_index
        self.debug = debug

        self.container = pudding.container.HorizontalContainer( \
                parent_widget, width=600, height=800, \
                left=self.left, top=self.top, z_index=1)

        self.container.add_child(pudding.control.SimpleLabel( \
                    parent_widget, label='', \
                    font=self.font, top=25, left=30))


    def _end(self):
        pass


    def update(self, subject):		
        if subject.data.status == 'roundStart':
            self.container.children[0].label = 'size: ' \
                + str(len(subject.data.song.lines))
        
        elif subject.data.status == 'end':
            self._end()
        elif self.debug:
            print 'status: ', subject.data.status


def main():
    pass

if __name__ == '__main__': main()

