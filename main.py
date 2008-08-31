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

import sys
import os

try:
	import psyco
	psyco.full()
except ImportError:
	print '+ Canta + Warning: Psyco not found. Performance will not be optimized.'
	pass

from canta.display.core_init import CoreInit


def main():
	# app name:
	APP_NAME = 'Canta'

	# app directory
	APP_DIR = os.path.dirname(sys.argv[0])

	# version:
	#if open(os.path.join(APP_DIR, 'VERSION')):
	version_file = open(os.path.join(APP_DIR, 'VERSION'))
	version = version_file.next()
	#else:
	#	version = '(experimental)'

	# debug flag:
	DEBUG = False

	# get platform info:
	PLATFORM = sys.platform

	# on Darwin systems:
	if 'darwin' in PLATFORM:
		from Authorization import Authorization, kAuthorizationFlagDestroyRights

	# on Windows systems:
	elif 'win32' in PLATFORM:
		import PIL.PngImagePlugin
		import PIL.JpegImagePlugin
	#	import win32com.client

	window_title = APP_NAME + ' ' + version
	CoreInit(window_title, APP_DIR ,DEBUG)

if __name__ == '__main__': main()

