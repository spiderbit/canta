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
from canta.theme.model import Model

class AniModel(Model):
	'''A class for Cal3D models.'''

	def __init__(self, parent_world=None, name='', position=(0.0, 0.0, 0.0), \
			scale=(1.0, 1.0, 1.0), rotation=(0.0, 0.0, 0.0), shadow=0, \
			action='', debug=0):

		self.debug = debug

		# call constructor of super class:
		Model.__init__(self, parent_world, name, position, scale, \
				rotation, self.debug)

		# set shadow:
		# TODO: get shadow state from config file.
		self.shadow = shadow

		# set action:
		self.action = action

		# create an animated model:
		animated_model = soya.AnimatedModel.get(self.name)

		# set shadow of the animated model:
		animated_model.shadow = self.shadow

		# create a body from the animated model:
		self.body = soya.Body(self.parent_world, animated_model)

		# start the animation cycle:
		self.body.animate_blend_cycle(self.action)

		# position, scale and rotate the body:
		self.set_position(self.position)
		self.set_scale(self.scale)
		self.set_rotation(self.rotation)

		# set name of the body:
		self.body.name = self.name

def main():

	DEBUG = 1

	import sys
	import os
	#import MovableCamera

	# init soya in resizable window:
	soya.init('Canta', 1024, 768, 0)

	# append our data path:
	soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), '..', 'data'))

	# disable soya's auto exporter:
	soya.AUTO_EXPORTERS_ENABLED = 0

	# set the root scene:
	scene = soya.World()

	# set up the light:
	light = soya.Light(scene)
	#light.set_xyz(1.0, 0.7, 1.0)
	light.set_xyz(0.0, 0.7, 1.0)

	# set up the camera:
	# (uncomment for static camera):
	camera = soya.Camera(scene)
	camera.set_xyz(0.0, 0, 10.0)

	# (uncomment for movable camera):
	#camera = MovableCamera.MovableCamera(scene)

	# create 5 animated objects (CANTA letters):
	# Letter 'C':
	name = 'Logo_0'
	position = (-4.0, 0.0, 0.0)
	scale = (4.0, 3.0, 3.0)
	rotation = (0.0, 0.0, 0.0)
	shadow = 1
	action = 'Logo_0Damping'
	test_animodel0 = AniModel(
				parent_world = scene,
				name = name,
				position = position,
				scale = scale,
				rotation = rotation,
				shadow = shadow,
				action = action,
				debug = DEBUG
				)
	# Letter 'A':
	name = 'Logo_1'
	position = (-3.0, -0.2, 0.0)
	scale = (1.0, 1.0, 1.0)
	rotation = (0.0, 0.0, 0.0)
	shadow = 1
	action = 'Logo_1Damping'
	test_animodel1 = AniModel(
				parent_world = scene,
				name = name,
				position = position,
				scale = scale,
				rotation = rotation,
				shadow = shadow,
				action = action,
				debug = DEBUG
				)

	# Letter 'N':
	name = 'Logo_2'
	position = (-1.5, 0.9, 0.0)
	scale = (1.0, 1.0, 1.0)
	rotation = (0.0, 0.0, 0.0)
	shadow = 1
	action = 'Logo_2Damping'
	test_animodel2 = AniModel(
				parent_world = scene,
				name = name,
				position = position,
				scale = scale,
				rotation = rotation,
				shadow = shadow,
				action = action,
				debug = DEBUG
				)
	# Letter 'T':
	name = 'Logo_3'
	position = (0.0, -0.5, 0.5)
	scale = (1.0, 1.0, 1.0)
	rotation = (0.0, 0.0, 0.0)
	shadow = 1
	action = 'Logo_3Damping'
	test_animodel3 = AniModel(
				parent_world = scene,
				name = name,
				position = position,
				scale = scale,
				rotation = rotation,
				shadow = shadow,
				action = action,
				debug = DEBUG
				)

	# Letter 'A':
	name = 'Logo_4'
	position = (2.0, 0.0, -0.3)
	scale = (1.5, 1.5, 1.5)
	rotation = (0.0, 0.0, 0.0)
	shadow = 1
	action = 'Logo_4Damping'
	test_animodel1 = AniModel(
				parent_world = scene,
				name = name,
				position = position,
				scale = scale,
				rotation = rotation,
				shadow = shadow,
				action = action,
				debug = DEBUG
				)

	# set our root widget:
	soya.set_root_widget(camera)

	# start soya main loop:
	soya.MainLoop(scene).main_loop()

if __name__ == '__main__': main()

