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

import sys
import os

from canta.song.song import Song

#from canta.song.player import Player
from canta.event.subjects.song_data import SongData

import soya

class SongEvent(soya.Body):
    """TODO!!
    """
    def __init__(self, song=Song(), widget_properties=None, song_data=0, \
            player=None, keyboard_event=None, input=None, debug=0):

        self.debug = debug
        self.song_data = song_data

        self.input = input

        self.keyboard_event = keyboard_event

        self.paused = False # is the Song paused
        self.song = song # song data (class song)
        self.song.line_nr = -1
        self.parent_world = widget_properties['root_world']

        self.msg = dict()
        self.msg['song'] = self.song

        # if its true i dont check for new song.events
        self.end_sended = False

        # i think the 4 is the resolution in the file but
        # i am not sure and 4 is default if nothing is given
        self.beat_time = 60. / song.info['bpm'] / 4
        self.status = None
        if self.debug: print "BUG:", (self.song.info['start']*1000)

        self.msg['beat_time'] = self.beat_time

        self.switch_time = - self.song.info['gap'] / 1000.    # for first row that it will be displayed instandly
        self.player = player

        self.current_note = None
        self.last_note = None
        self.status = ""
        self.old_line_nr = None



    # that must in a big loop for events from the file from
    # the keyboard and from the microphone
    def begin_round(self):
        pos = self.player.get_pos()
        if not pos:
            return
        if self.debug: print "start: ",self.song.info['start']
        if not self.end_sended:
            if not self.player.paused:
                if pos != 'end':
                    self.real_pos_time = self.player.get_pos() \
                        - self.song.info['gap'] / 1000. # position in the song
                    self.msg['real_pos_time'] = self.real_pos_time
                    self.msg['player'] = self.player
                    self.msg['type'] = "roundStart"
                    self.song_data.set_data(self.msg) # round Event
                #if self.start:
                self._check_for_next_line(pos) # check for nextLine Event

        else:
            self.parent_world.remove(self)
            self.input.stop()
            self.input.join(0.1)

    def _check_for_next_line(self, pos): # check for next Line


        if pos != "pause":

            self.song.line_nr, self.current_note = self.song.get_pos(pos)#old_line_nr=self.old_line_nr, old_tone_nr=self.last_note)

            if pos == 'end':
                self.parent_world.remove(self.keyboard_event)
                self.msg['type'] = "end"
                self.song_data.set_data(self.msg) # end Event
                self.song.end = True
                self.end_sended = True

            elif self.song.line_nr != None:
                if self.song.line_nr != self.old_line_nr:


                    self.msg['type'] = "nextLine"
                    #subject.data['song'].line_nr
                    self.song_data.set_data(self.msg)
                    self.old_line_nr = self.song.line_nr
                    self.last_note = None



                elif self.current_note != self.last_note and self.old_line_nr == self.song.line_nr:	# geänderte aktuelle note

                    if  self.last_note != None and 1 == 1: # überprüfen wegen deaktivieren von der letzten note
                        #print "deactivate note:", self.last_note, " aktual-note:", self.current_note, self.song.lines[self.song.line_nr].segments[self.last_note].text

                        self.msg['type'] = "deActivateNote"
                        self.msg['old_pos'] = self.last_note
                        self.song_data.set_data(self.msg) # deactivate event

                    if self.current_note != None and 1 == 1: # überprüfen wegen aktivierung einer note
                        #print "  activate note:", self.current_note, " aktual-note:", self.current_note, self.song.lines[self.song.line_nr].segments[self.current_note].text

                        self.msg['type'] = "activateNote"

                        self.msg['pos'] = self.current_note
                        self.song_data.set_data(self.msg)

                    self.last_note = self.current_note

