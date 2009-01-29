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

class DisplayProperties:
    def __init__(self):
        # default is 1024x768. applies if user wrote an invalid
        # res into config file by hand...
        self.selected_resolution = 2
        self.valid_resolutions = ['300x200', '320x480', '640x400', '640x480', \
                    '800x480', '800x600', '1024x600','1024x768', \
                    '1280x720', '1280x800', '1280x1024', \
                    '1400x1050', '1440x900', '1600x1200', '1680x1050', '1920x1200']
        self.active_resolution = self.valid_resolutions[self.selected_resolution]


#	def select_next(self):
#		"""Select the next solution in the list of valid resolutions.
#			If the end of the list is reached, start at the beginning again.
#		"""
#		pass
#		if self.selected_resolution + 1 > len(self.valid_resolutions) - 1:
#			self.selected_resolution = 0
#		else:
#			self.selected_resolution = self.selected_resolution + 1
#
#		self.active_resolution = self.valid_resolutions[self.selected_resolution]


def main():

    disp = DisplayProperties()
    print 'valid resolutions:', disp.valid_resolutions
    print 'active resolution:', disp.active_resolution
#	print

#	for i in range(10):
#		print 'select_next()'
#		disp.select_next()
#		print disp.active_resolution

if __name__ == '__main__': main()

