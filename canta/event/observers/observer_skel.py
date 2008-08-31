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




class MainCubeObserver:
	def __init__():
		pass

	def _next_line(self, song):	
		pass
		

	def update(self, subject):
		status = subject.data['type']
		if status == 'roundStart':
			pass
		elif status == 'activateNote':
			self._activate_note(subject.data['pos'])
		elif status == 'deActivateNote':
			self._de_activate_note(subject.data['old_pos'])
		elif status == 'nextLine':
			self._next_line(subject.data['song'])
		elif status == 'end':
			self._end()
		elif self.debug:
			print 'status: ', status

