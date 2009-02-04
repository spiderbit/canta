#!/usr/bin/python -O
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

"""Module song_line

Classes: SongLine
"""


class SongLine:
    """SongLine consist of:

    - show_time     the time when the line should be displayed
    - segments[]    the notes type: SongSegment
    """
    def __init__(self, show_time=0):
        """Constructor"""
        self.show_time = show_time
        self.segments = []

    def add_segment(self, song_segment):
        """Add a segment"""
        self.segments.append(song_segment)

    def remove_segment(self, pos):
        """Remove segment <pos>"""
        del self.segments[pos]


    def __cmp__(self, other):
        """Returns True if other and self have identical attributes"""

        if self.__dict__ == other.__dict__:
            return True
        else:
            return False
