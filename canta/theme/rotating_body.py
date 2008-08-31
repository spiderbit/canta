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
import os.path
import soya

class RotatingBody(soya.Body):
	'''A simple soya body that rotates around y axis.'''

	def __init__(self, parent_world=None, model=None, sens=1.0, \
			rotation='z', debug=False):

		self.debug = debug

		soya.Body.__init__(self, parent_world, model)
		self.sens = sens

		if rotation == 'x':
			self.func = self.rotate_x
		elif rotation == 'y':
			self.func = self.rotate_y
		else:
			self.func = self.rotate_z

	def advance_time(self, proportion):
		soya.Body.advance_time(self, proportion)
		self.func(proportion * 1.0 * self.sens)

if __name__ == '__main__':

	DEBUG = 1

	import sys
	import os
	import soya.cube

	# init soya in resizable window:
	soya.init('Canta', 1024, 768, 0)

	# set the root scene:
	scene = soya.World()

	# create a test cube model:
	test_cube_world = soya.cube.Cube()
	#test_cube_world.model_builder = soya.SolidModelBuilder()
	test_cube = test_cube_world.to_model()

	rotation_speed = 2.0
	# create an instance of the class:
	test_rotating_body = RotatingBody(
				parent_world = scene,
				model = test_cube,
				sens = rotation_speed,
				debug = DEBUG
				)

	# set up the light:
	light = soya.Light(scene)
	light.set_xyz(0.0, 0.7, 1.0)

	# set up the camera:
	camera = soya.Camera(scene)
	camera.set_xyz(0.0, 0, 10.0)

	# set our root widget:
	soya.set_root_widget(camera)

	# start soya main loop:
	soya.MainLoop(scene).main_loop()

