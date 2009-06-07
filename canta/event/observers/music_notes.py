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
import os

from canta.event.observers.cube_list import CubeList
from canta.theme.panel import Panel

class MusicNotes:
    def __init__(self, parent_world, position=(0., 5., 2.0), scale=(9.6, 1.2, 1.2)):
        self.parent_world = parent_world
        self.world = soya.World()
        self.parent_world.add(self.world)
        self.scale = scale
        self.position = position
        self.panel = None


    def load_texture(self, nr):
        '''loads the texture of sheet music of one line'''
        media_path = os.path.join(self.song.path, 'media')
        tex_path = os.path.join(media_path, 'images')
        if os.path.exists(tex_path):
            soya.path.append(media_path)
            # Texture file names must begin with text file name.
            # Not very nice but a quick hack bugfix.
            file_name = "%s%s.png" % \
                    (self.song.reader.file_name[:-4] , nr)
            file_name_abs = os.path.abspath( \
                    os.path.join(tex_path, file_name))
            if os.path.isfile(file_name_abs):
                return file_name_abs


    def _end(self):
        self.parent_world.remove(self.world)


    def _draw_line(self, line_nr):
        texture = self.load_texture(line_nr)
        if texture:
            if not self.panel:
                self.panel = Panel(self.world, scale=self.scale, \
                    position=self.position, texture=texture)
            else:
                self.panel.update_texture(texture)


    def update(self, subject):
        status = subject.data['type']
        if status == 'roundStart':
            pass
        elif status == 'activateNote':
            pass
        elif status == 'deActivateNote':
            pass
        elif status == 'nextLine':
            self.song = subject.data['song']
            self._draw_line(subject.data['song'].line_nr)
        elif status == 'end':
            self._end()

