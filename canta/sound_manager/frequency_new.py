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

import numpy
import wave
import time
import random

class Frequency:
    """Read a sample from the soundcard, do the FFT on the sample and return
        frequency.
    """
    def __init__(self, soundManager, fftManager):
        self.smo = soundManager
        self.fft = fftManager

        # Min and max possible frequencies (human voice range):
        self.min_freq = 73.0
        self.max_freq = 1396.0

    def get_disabled(self):
        time.sleep(0.1)
        return random.uniform(0,30)

    def get(self):

        chunk = 1024

        # We take a sample from the soundcard. The sample is in binary form.
        data = self.smo.readData(chunk)

        # Unpack (convert from binary to int (or float?)) the sample.
        data_length = str(len(data)) + 'B'
        sig = wave.struct.unpack(data_length, data)

        # We make use of the rfft() function, which is optimized for real
        # (as opposed to complex) data.
        # Using 10*log10(abs( converts the energy measurements of the FFT into energy
        # on a logarithmic scale called decibels. This is better suited for displaying
        # signal power.
        # The addition of the constant (1E-20) solves the problem of log10(0) being undefined.
        # Rather than check each argument for 0, we just add a small inconsequential value to
        # guarantee that the 0 case never arises. There is a lot of work going on here.
        # This is where the muscle is applied. The result is an array that contains the energy
        # values found in each of the frequencies across the sample (sections of the
        # time signal).
        y_range = 10 * numpy.log10(1e-20 + abs(self.fft.doFFT(sig)))

        time.sleep(0.1)

        # The output only contains 512 outputs from the original 1024 input values.
        # Because the FFT is designed for complex data (containing both a real and
        # an imaginary component), and we are using real data, the output is symmetric.
        # The missing 512 samples are simply replicas of the first 512 in the output sequence.
        # The rfft() function we are using knows this and saves effort by not computing them.
        # The value with index 0 seemed to be fucked up (its power was always the one with the
        # greatest power), so we cut it away.
        y = y_range[1:513]

        max = 0
        index = 0

        for i, value in enumerate(y):
            if value > max:
                max = value
                index = i


        # / chunk there was 1024 so i think its also the chunk size
        # if that code does not work with other chunk size it could be not chunk size and was fix 1024
        # but i believe it must be chunk size and the /2 and the * 2 in the next 2 lines could be
        # not needed 
        # should not be integer i think so if you remove the 2 make shure that its no integer division
        f = self.smo.sampling_frequency / 2. / chunk			
        
        frequency = (index + 1) * f * 2

        # Check if the frequency we got is in range of the human voice.
        # Do we need this!?
        if frequency < self.min_freq or frequency > self.max_freq:
            frequency = None

        return frequency


def main():
    a = SoundManagerOSS()
    #a = SoundManagerPyAudio()
    b = FFTNumPy()
    x = Frequency (a, b)

    while(True):
        temp = x.getFrequency()
        print (temp)


if __name__ == '__main__': main()

