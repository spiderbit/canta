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

from sound_manager import SoundManager
from ossaudiodev import *

class SoundManagerOSS:
    """TODO.
    """
    def __init__(self, sampling_frequency):
        # Open Soundcard.
        # open([device, ]mode): if device is not specified, environment
        # variable AUDIODEV is used.
        # Falls back to /dev/dsp if not defined. mode can be 'r', 'w', 'rw'.
        self.dsp = open('r')
        format = AFMT_S16_LE
        channels = 1
        self.sampling_frequency = sampling_frequency
        self.dsp.setparameters(format, channels, self.sampling_frequency)

    def readData(self, number_of_samples=1024):
        return self.dsp.read(number_of_samples)


    def start(self):
        print "not implemented yet"

    def stop(self):
        print "not implemented yet"
