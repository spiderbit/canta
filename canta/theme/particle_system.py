#! /usr/bin/python -O
# -*- coding: utf-8 -*-
#
#    CANTA - A free entertaining educational software for singing
#    Copyright (C) 2007  S. Huchler, A. Kattner, F. Lopez
#
#    Class from Soya 3D tutorial
#    Copyright (C) 2001-2004 Jean-Baptiste LAMY
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

from random import random
from math import sqrt
from soya import sdlconst
#from soya import particle
from soya import Smoke, FlagSubFire, FlagFirework, Particles


class ParticleSystem(Smoke):
	def __init__(self,parent):
		Particles.__init__(self,parent,nb_max_particles=50)
		self.auto_generate_particle = 1

	def generate(self, index):
		sx = (random()- 0.5) * .2
		sy = (random())
		sz = (random() - 0.5) * .2
		l = (0.2 * (1.0 + random())) / sqrt(sx * sx + sy * sy + sz * sz) * 0.5
		self.set_particle(index, random()*.5, sx * l, sy * l, sz * l, 0.,0.,0.)

