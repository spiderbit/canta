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
from canta.song.song_segment import SongSegment

class SingCubeObserver(CubeObserver):
    def __init__(self, parent_world, color, color_formula, min_pitch=0., \
        max_pitch=11., game=None):
        CubeObserver.__init__(self, parent_world, min_pitch, max_pitch)
        self.color = color
        self.color_formula = color_formula
        self.game = game

    def input(self, data):
        '''Calculates the possible/lost/gathered points and returns it'''
        pitch = data['pitch']
        target_tone = data['song'].get_tone_between( \
            data['start_time'], data['end_time'])
        if not target_tone or not isinstance(target_tone, SongSegment):
            return
        elif pitch:
            '''sang'''
            if target_tone.freestyle:
                '''freestyle'''
                self.hit_tone(data, target_tone.pitch, 0)
            else:
                pitch = self.game.get_corrected_pitch(target_tone.pitch, pitch)
                difference = abs(target_tone.pitch - pitch)
                if self.game.helper:
                    '''helper on'''
                    if difference <= self.game.allowed_difference:
                        '''sang within allowed diff'''
                        self.hit_tone(data, pitch, difference)
                    else:
                        '''sang not within allowed diff'''
                        self.missed_tone(data, pitch, difference)
                elif difference == 0:
                    '''helper off but hit exactly the pitch'''
                    self.hit_tone(data, pitch, difference)
                else:
                    '''helper off and not hit pitch'''
                    self.missed_tone(data, pitch, difference)
        else:
            '''not sang'''
            self.not_sang(data)


    def get_type(self, data):
        '''
            get the type of the target_tone as string,
            i think it would be better if
            song_segment has a string like that
            instead the 2 seperate attribs
        '''
        target_tone = data['song'].get_tone_between( \
            data['start_time'], data['end_time'])
        if target_tone.freestyle:
            _type='freestyle'
        elif target_tone.special:
            _type='bonus'
        else:
            _type='normal'
        return _type

    def hit_tone(self, data, pitch, difference):
        self.draw(data, 0, pitch)
        _type = self.get_type(data)
        self.game.add_stat(_type, hit=True)

    def missed_tone(self, data, pitch, difference):
        self.draw(data, difference, pitch)
        _type = self.get_type(data)
        self.game.add_stat(_type, hit=False)

    def not_sang(self, data):
        _type = self.get_type(data)
        self.game.add_stat(_type, hit=False)


    def draw(self, data, difference, pitch, properties=None):
        self.calc_start_end_size(data['song'])
        time_stamp = data['real_pos_time']/data['beat_time']
        duration = data['length_in_beats']
        if properties == None:
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
            self.input(subject.data)

