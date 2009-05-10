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

from canta.event.observers.cube_observer import CubeObserver

class SingCubeObserver(CubeObserver):
    def __init__(self, parent_world, color, color_formula, min_pitch=0., \
        max_pitch=11., game=None, debug=0):
        CubeObserver.__init__(self, parent_world, min_pitch, max_pitch, debug)
        self.color = color
        self.color_formula = color_formula
        self.game = game

    def input(self, data):
        target_pitch = data['song'].get_pitch_between( \
            data['start_time'], data['end_time'])
        if not target_pitch:
            return

        pitch = data['pitch']
        pitch = self.game.get_corrected_pitch(target_pitch, pitch)
        difference = pitch - target_pitch

        if not self.calc_start_end_size(data['song']):
            return False

        time_stamp = data['real_pos_time']/data['beat_time']
        duration = data['length_in_beats']

        properties = {}
        properties['length'] = duration
        properties['rotate'] = False

        col = []
        for x in range(len(self.color)):
            diff = (self.color_formula[x] / 100.) * difference
            tmp = self.color[x] +  diff
            if tmp < 0:
                tmp = 0
            elif tmp > 1:
                tmp = 1
            col.append(tmp)

        properties['diffuse'] = col
        self.draw_tone(time_stamp, pitch, duration, properties)

    def get_corrected_pitch(self, target_pitch, pitch):
        '''
            gives back pitch on target_pitch if the difference to it
            is smaller then allowed_difference
        '''
        difference = pitch - target_pitch
        if abs(difference) <= self.allowed_difference:
            pitch = target_pitch
        return pitch


    def update(self, subject):
        status = subject.data['type']
        if status == 'roundStart':
            pass
        elif status == 'activateNote':
            pass
        elif status == 'deActivateNote':
            pass
        elif status == 'nextLine':
            self._delete_all()
        elif status == 'end':
            self._end()
        elif status == 'input':
            if subject.data['pitch']:
                self.input(subject.data)
        elif self.debug:
            print 'status: ', status

