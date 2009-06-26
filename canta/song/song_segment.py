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

class SongSegment:

    def __init__(self, type, time_stamp, duration=0, pitch=0, text="", special=False, freestyle=False):

        self.type = type #( note, pause, end )
        self.time_stamp = time_stamp
        self.duration = duration
        self.pitch = pitch
        self.text = text
        self.special = special # note + special = bonus
        self.freestyle = freestyle


    def __eq__(self, other):
        """Returns True if other and self have identical attributes"""

        if isinstance(other, SongSegment) and self.__dict__ == other.__dict__:
            return True
        else:
            return False

