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

import pygame
import os,sys


class ClickObserver:
	def __init__(self, click_sound):
		pygame.mixer.pre_init(44100,-16,2, 1024 * 3)
		pygame.mixer.init()
		#pygame.mixer.music.set_volume(0.50)	
		#pygame.mixer.music.load(os.path.join()
		#self.sound = pygame.mixer.Sound(click_sound)

	def click(self):
		self.sound.play()


	def _next_line(self, song):	
		pass
		#sound

	def update(self, subject):
		status = subject.data['type']
		if status == 'roundStart':
			pass
		elif status == 'activateNote':
			self.click()
		elif status == 'deActivateNote':
			self.click()
		elif status == 'nextLine':
			pass
		elif status == 'end':
			pass
		elif self.debug:
			print 'status: ', status

