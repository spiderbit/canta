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



import math
import soya

from canta.event.observers.cube_list import CubeList

class CubeObserver(CubeList):
    """Draw bars with different positions and lengths.
        The bars represent notes with different pitches
        and durations.
        TODO: 	* rename to BarSomething coz cube is to general.
            * add an underscore to variables that clash with
            python specific keywords (e.g. min -> min_)
    """
    def __init__(self, parent_world, min_pitch=0., max_pitch=11., \
                 size_x=0.3, size_y=0.2):
        CubeList.__init__(self, parent_world)
        # These 2 values could also be a paramter for draw_tone
        # (if it seems to be better?)
        # They are size of 1 beat (x and y) (z is constant):
        self.size_y = size_y
        self.size_x = size_x

        # Minimum and maximum pitch that occurs in this line:
        self.min_pitch = min_pitch
        self.max_pitch = max_pitch

        # Count of different pitches in line:
        self.number_of_different_tones = self.max_pitch - self.min_pitch

        # Define the size of the line. How can we get the whole size of x?
        # we would need from the camera
        #	1. the distance
        #	2. the viewangle
        #	3. the size of projection (if distance is zero)
        self.size_of_window_x = 15.

        # Distance to the left in beats.
        # You get the width of a line by calculating beats * size_x
        self.distance_from_side = 0


    def calc_start_end_size(self, song):	# these values differ only from line to line

        line_nr = song.line_nr
        if line_nr == None:
            return False
        show_time = song.lines[line_nr].show_time

        #start_x is the first time_stamp in beats
        self.start_x = float(song.lines[line_nr].segments[0].time_stamp \
                - self.distance_from_side)

        #end_x is the distance from the last segment (incl. duration) from the first in beats
        self.end_x = float(song.lines[line_nr].segments[-1].time_stamp \
                + song.lines[line_nr].segments[-1].duration \
                + self.distance_from_side - self.start_x)
        if self.end_x != 0:

            self.size_x = self.size_of_window_x / self.end_x
        else:
            self.size_x = 1
        return True


    def draw_tone(self, time_stamp, pitch, duration, properties):	# these values differ from tone to tone


        position_y = (0 - (self.number_of_different_tones / 2) \
                    + (pitch - self.min_pitch) + 0.5) * self.size_y		# 0.5 for half length
        position_x = (0 - (self.end_x / 2 ) + (time_stamp - self.start_x) \
                    + (duration / 2)) * self.size_x
        position_z = 0

        properties['x'] = position_x
        properties['y'] = position_y
        properties['z'] = position_z
        properties['specular']=False
        properties['seperate_specular']=False

        self.add(properties)

