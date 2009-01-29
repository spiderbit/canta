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


import soya
import math

from canta.event.observers.cube_list import CubeList
from canta.theme.panel import Panel

class MusicNotes:
    def __init__(self, parent_world, textures=[], position=(0., 0., 0.), \
            scale=(1., 1., 1.), debug=0):
        self.debug = debug
        self.parent_world = parent_world
        self.world = soya.World()
        self.parent_world.add(self.world)
        self.textures = textures
        self.scale = scale
        self.position = position
        self.active_texture = -1
        self.panel = Panel(self.world, scale=self.scale, \
                position=self.position, texture=self.textures[0])
        

    def _end(self):
        self.parent_world.remove(self.world)


    def _draw_next_line(self):
        self.active_texture += 1
        if self.active_texture == len(self.textures):
            self.active_texture = 0
        else:
            pass
        self.panel.update_texture(self.textures[self.active_texture])


    def update(self, subject):
        status = subject.data['type']
        if status == 'roundStart':
            pass
        elif status == 'activateNote':
            pass
        elif status == 'deActivateNote':
            pass
        elif status == 'nextLine':
            self._draw_next_line()
        elif status == 'end':
            self._end()
        elif self.debug:
            print 'status: ', status

