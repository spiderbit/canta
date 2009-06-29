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


import os
import wave
from time import time
from player import Player
import canta.metadata as metadata

class DummyPlayer(Player):

    def __init__(self, path=None, file=None, time=0.0):
        Player.__init__(self, path, file, time=0.0)
        self.loaded = False
        self.pos = 0.0

    def load(self, path=None, file=None):
        self.loaded = True
        if path:
            self.path=path
        if file:
            self.file=file
        f = metadata.get_format(os.path.join(self.path, self.file))
        if f is None:
            print "format not supported"
        else:
            self.length = f.get_length()

    def play(self, start=0):
        if self.paused and start == 0:
            self.paused = False
            self.start_time = time()

        elif self.loaded:
            self.start_time = time()
        self._play()
        print "play"

    def get_pos(self):
        if self.paused:
            return "pause"
        elif self.length > self.pos + (time() - self.start_time):
            return self.pos + (time() - self.start_time)
        else:
            self.pos = 0.0
            return "end"


    def get_duration(self):
        """Returns the duration of the song in seconds"""
        return self.length

    def pause(self):
        self.pos += time() - self.start_time
        self._pause()
        print "pause"

    def play_freq(self, freq):
        print "BEEP, you choose the dummy player so will hear nothing!"

    def stop_freq(self):
        print "<stop> BEEP"

    def stop(self):
        self.running = False
        self.pos = 0.0
        print "stop"

