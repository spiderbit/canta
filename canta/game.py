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
    '''
        this class is for Game settings or methods
        that are needed to work with them
    '''
    def __init__(self, config):
        self.octave = config['misc'].as_bool('octave_adjusting')
        # if helper is set you only need to sing nearly the right tone
        self.helper = config['misc'].as_bool('easier_tone_hitting')
        self.allowed_difference = config['misc'].as_int('allowed_difference')
        self.stats = {}
        self.stats['normal'] = {'hits' : 0, 'misses' : 0, 'points' : 100}
        self.stats['bonus'] = {'hits' : 0, 'misses' : 0, 'points' : 200}
        self.stats['freestyle'] = {'hits' : 0, 'misses' : 0, 'points' : 100}

    def get_corrected_pitch(self, target_pitch, pitch):
        if not self.octave:
            pitch = self.octave_correction(target_pitch, pitch)
        return pitch

    def octave_correction(self, target_pitch, pitch):
        ''' change octave of pitch so that it's nearest to target_pitch '''
        same_octave = False
        while not same_octave:
            difference = pitch - target_pitch
            if difference > 6:
                pitch -= 12
            elif difference < -6:
                pitch += 12
            else:
                same_octave = True
        return pitch

    def add_stat(self, _type, hit):
        if hit:
            self.stats[_type]['hits']+=1
        else:
            self.stats[_type]['misses']+=1


    def get_points(self, _type='sum', target='hits'):
        points = 0
        if _type == 'sum':
            for k,v in self.stats.iteritems():
                points += v[target] * v['points']
        else:
            points = self.stats[_type][target] * self.stats[_type]['points']
        return points

    def get_points_possible(self, _type='sum'):
        return self.get_points(_type=_type) + self.get_points(_type=_type, target='misses')

