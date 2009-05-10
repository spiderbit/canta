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


class Game:
    def __init__(self, octave=True, helper=True, allowed_difference=1):
        self.octave = octave
        self.helper = helper
        self.allowed_difference = allowed_difference

    def get_corrected_pitch(self, target_pitch, pitch):
        if not self.octave:
            pitch = self.octave_correction(target_pitch, pitch)
        return pitch

    def octave_correction(self, target_pitch, pitch):
        ''' change octave of pitch so that it's nearest to target_pitch '''
        same_octave = False
        while not same_octave:			# that code do all tones display on same octave
            difference = pitch - target_pitch
            if difference > 6:
                pitch -= 12
            elif difference < -6:
                pitch += 12
            else:
                same_octave = True
        return pitch

