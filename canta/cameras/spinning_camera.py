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

class SpinningCamera(soya.Camera):
    def __init__(self, parent, look_at):
        soya.Camera.__init__(self, parent)
        self.angle = 0.0
        self.obj_look_at = look_at


    def advance_time(self, proportion):
        if self.angle > 359.0: self.angle = 0.0
        else: self.angle += 0.15

        degrees = self.angle * 2.0
        radians = degrees * (math.pi / 180.0)
        self.set_xyz(20.0 * math.cos(radians), 0, -20.0 * math.sin(radians))
        self.look_at(self.obj_look_at)

