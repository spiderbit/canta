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
import pyaudio
import wave
import sys

format = pyaudio.paInt16
channels = 1
chunk = 1024

class SoundManagerPyAudio:
    """Create a PyAudio object and open a stream to read from.
    """
    def __init__(self, sampling_frequency=11025):
        self.p = pyaudio.PyAudio()
        self.sampling_frequency= 11025

    def start(self):
        self.stream = self.p.open(format=format, channels=channels, \
                rate=self.sampling_frequency, input=True, \
                frames_per_buffer=chunk)


    def readData(self, number_of_samples=1024):
        return self.stream.read(number_of_samples)


    def stop(self):
        self.stream.close()


