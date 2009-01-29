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

class Model:
    """An (abstract) parent class for all the other model classes.
    """

    def __init__(self, parent_world=None, name=None, position=(0.0, 0.0, 0.0), \
            scale=(1.0, 1.0, 1.0), rotation=(0.0, 0.0, 0.0), debug=0):

        self.debug = debug
        self.parent_world = parent_world
        self.name = name
        self.position = position
        self.scale = scale
        self.rotation = rotation
        self.body = None


    def set_position(self, position):
        self.body.set_xyz(position[0], position[1], position[2])


    def set_scale(self, scale):
        self.body.scale(scale[0], scale[1], scale[2])


    def set_rotation(self, rotation):
        self.body.rotate_x(rotation[0])
        self.body.rotate_y(rotation[1])
        self.body.rotate_z(rotation[2])


def main():
    pass

if __name__ == '__main__': main()

