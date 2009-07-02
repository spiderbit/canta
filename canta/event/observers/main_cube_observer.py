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


from canta.event.observers.cube_observer import CubeObserver

class MainCubeObserver(CubeObserver):
    def __init__(self, parent_world, color, min_pitch=0., max_pitch=11.):
        CubeObserver.__init__(self, parent_world, min_pitch, max_pitch)
        self.color = color



    def _next_line(self, song):
        """Draw the whole line that is selected (song.line_nr).
            pitch = (integer) pitch value from File
            words = list of SongSegments
        """

        properties = {}




        line_nr = song.line_nr
        self.calc_start_end_size(song)
        for word in song.lines[line_nr].segments:

            properties['length']=word.duration

            properties['rotate'] = False
            if word.special:
                properties['diffuse'] = self.color['special']
            elif word.freestyle:
                properties['diffuse'] = self.color['freestyle']
            else:
                properties['diffuse'] = self.color['normal']


            self.draw_tone(word.time_stamp, word.pitch, word.duration, properties)


    def update(self, subject):
        status = subject.data['type']
        if status == 'roundStart':
            pass
        elif status == 'activateNote':
            #if self.debug:
            #	print subject.data['pos']
            self._activate_note(subject.data['pos'])
        elif status == 'deActivateNote':
            #if self.debug:
            #	print subject.data['old_pos']
            self._de_activate_note(subject.data['old_pos'])
        elif status == 'nextLine':
            self._delete_all()
            self._next_line(subject.data['song'])
        elif status == 'end':
            self._end()

