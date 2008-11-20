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
 
import pygame
import pygame.mixer
import os
import time
import random

import math

NUM_IMPL = 'numeric'

# needs to be tested:
#if pygame.version.vernum > (1,8):
#	NUM_IMPL = 'numpy'

if NUM_IMPL == 'numeric':
	import Numeric as N
elif NUM_IMPL == 'numpy':
	import numpy
from player import Player

class PygamePlayer(Player):
	
	def __init__(self, path=None, file=None, time=0.0):
		Player.__init__(self, path, file, time)
		self.samples_per_sec = 44100
		self.bits_per_sample = 16
		self.loaded = False
		if file != None:
			self.load(path, file)

	def load(self, path=None, file=None):
		self.loaded = True
		if path != None:
			self.path=path
		if file != None:
			self.file=file
		pygame.mixer.pre_init(self.samples_per_sec, -self.bits_per_sample, 1, 1024 * 3)
		pygame.mixer.init()
		pygame.mixer.music.set_volume(0.50)
		tmp = os.path.join(self.path, self.file).encode('utf-8')
		pygame.mixer.music.load(tmp)

	def stop(self):
		if pygame.mixer.get_init():
			pygame.mixer.music.stop()
		
	def fadeout(self):
		pygame.mixer.music.fadeout(2)

	def play(self, start=0):
		if self.paused and start==0:
			pygame.mixer.music.unpause()
		elif self.loaded:
			if start != 0 and not self.file[-3:].upper() == 'OGG':
				print "[WARNING] this player supports the used function " \
					+ "only for ogg audio files, use another player"
				return
			pygame.mixer.music.play(0, start)
		self._play()


	def get_pos(self):
		if self.paused:
			return "pause"
		elif pygame.mixer.music.get_pos() != -1:
			return float(pygame.mixer.music.get_pos()) /1000. + self.time
		else:
			return "end"

	def pause(self):
		pygame.mixer.music.pause()
		self._pause()


	def play_freq(self, freq):
		self.beep = self.make_tone(freq, duration=1)
		self.beep.play()

	def stop_freq(self):
		self.beep.stop()


	def make_tone(self, frequency=240, duration=1, fade_cycles=0):
		samples_per_cycle = int(math.ceil(float(self.samples_per_sec) / frequency))
		total_samples = samples_per_cycle * int(frequency * duration)
		if NUM_IMPL == 'numeric':
			samples = N.zeros(total_samples, N.Int16)
		# needs to be tested:
		#elif NUM_IMPL == 'numpy':
		#	pygame.sndarray.use_arraytype(numpy)
		#	samples = numpy.core.zeros(total_samples)
		amplitude = ((2 ** self.bits_per_sample) / 2) - 1
		k = 2.0 * math.pi / samples_per_cycle
		for i in range(total_samples):
			samples[i] = int(amplitude * math.sin(k * (i % samples_per_cycle)))	
		fade_samples = samples_per_cycle * fade_cycles
		start_fade = total_samples - fade_samples
		for i in range(fade_samples):
			samples[start_fade+i] = int(samples[start_fade+i]*float(fade_samples-i)/fade_samples)
		res = pygame.sndarray.make_sound(samples)
		res.set_volume(1.0)
		return res


def main():
	import sys,time
	player = PygamePlayer(file=sys.argv[1])
	player.load()
	player.run()
	time.sleep(20)


if __name__ == '__main__': main()
