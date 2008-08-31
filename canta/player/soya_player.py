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
import time

from player import Player


class SoyaPlayer(Player):
	
	def __init__(self, parent=None, path="", file="", time=0.0):
		Player.__init__(self, path, file, time)
		self.parent = parent
		#soya.init(sound = 1)
		#soya.set_sound_volume(1.0)
		# better make this append in load and then get the file and then remove it, its cleaner
		soya.path.append(self.path)
		soya.Sound.DIRNAME = ""
		self.sys_time = 0
		
		
	def load(self):
		#print self.path
		print self.file
		self.sound = soya.Sound.get(self.file)

		
	def play(self):
	
		sound_player = soya.SoundPlayer(self.parent, self.sound, \
				loop=0, play_in_3D=False, auto_remove=True)
		self.sys_time = time.time()
		self._play()
	

	def get_pos(self):
		if (self.paused):
			return self.time
		else:
			return self.time + time.time() - self.sys_time

			
	# not implemented right yet, to hard we must programm directly in openal
	def pause(self):
		print "<PAUSE>"
		print "time vor: ", self.time
		#self.time = self.time + sys.time
		print "time nach: ", self.time
		self._pause()

