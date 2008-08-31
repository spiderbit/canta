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
 
import pyaudio
import ogg.vorbis
import sys
from threading import Thread
import os
import time

from player import Player

class PyaudioPlayer(Player, Thread):
	

	# here instead of file it could be given the song object
	# then the get_pos could give the real_pos (without gap...)
	def __init__(self, path="", file = "", time = 0.0):		
		Player.__init__(self, path, file, time)
		Thread.__init__(self)
		self.chunk = 512
		PyAudio = pyaudio.PyAudio

		self.vf = ogg.vorbis.VorbisFile(os.path.join(self.path, self.file))
		vc = self.vf.comment()
		self.vi = self.vf.info()
		
		self.p = PyAudio()
		
		# open stream
		self.stream = self.p.open(format = pyaudio.paInt16, \
				#p.get_format_from_width(2), # could work with 8 16 24??
				channels = self.vi.channels, \
				rate = self.vi.rate, output = True)

                self.count=0
                self.sys_time = 0
                

	def load(self):
		#pygame.mixer.music.load(os.path.join(self.path, self.file))
		pass

	def play(self):
		self.sys_time = time.time()
		self.start()
		self._play()
		


	def run(self):
		while 1:
			(buff, bytes, bit) = self.vf.read(self.chunk)
			# play stream
			if bytes == 0:
				break
			self.stream.write(buff)
			time.sleep(0.0005)
			#self.count +=1
			#self.totalBytes += bytes

		self.stream.stop_stream()
		self.stream.close()
		
		self.p.terminate()
		self._play()
		
	def get_pos(self):
		#print "not implemented yet"
		#self.time += 0.1
		#return self.time
		
		#time = float(self.count) * self.chunk / self.vi.rate
		#print time
		#return time


                #print time.time() - self.sys_time

		if (self.paused):
			return self.time
		else:
			return self.time + time.time() - self.sys_time

		
		

	def pause(self):
		print "not implemented yet"

