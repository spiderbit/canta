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
import math

from canta.event.observers.cube_observer import CubeObserver
#from canta.theme.rotating_body import RotatingBody

class PosCubeObserver(CubeObserver):
    def __init__(self, parent_world, color, debug = 0):
        #CubeList.__init__(self, parent_world, min, max, debug)
        CubeObserver.__init__(self, parent_world, debug)

        self.distance_from_side = 0		# could be problematic must be sync with the other observers
        self.debug = debug
        self.parent_world = parent_world
        self.world = soya.World()
        self.parent_world.add(self.world)

        self.model_builder = soya.SimpleModelBuilder()
        self.model_builder.shadow = 1

        self.material = soya.Material()
        self.material.environment_mapping = 1
        self.material.diffuse = color
        #(1.0, 1.0, 1.0, 0.3)

        ### SHINYNESS ^^ ###
        #self.material.texture = soya.Image.get("env_map.jpeg")
        ### END SHINYNESS ^^ ###

        self.size_of_window_x = 15

        self.range_x = 5

        # For the pos cube.
        self.size_x = 0.1
        bar = soya.cube.Cube(material=self.material)
        bar.scale(self.size_x, 1, 1)

        #bar.model_builder = self.model_builder

        model = bar.to_model()

        self.pos_cube = soya.Body(self.world, model)
        #self.pos_cube = RotatingBody(self.world, model)


    def _update_pos_bar(self, data):

        song = data['song']
        line_nr = song.line_nr
        self.calc_start_end_size(song)
        line_pos = data['real_pos_time'] - (self.start_x * data['beat_time'])

        if self.start_x >= 0:
            #print linePos * 100 / time_between , "%"

            position_x = ((line_pos / data['beat_time'] + (self.size_x /2)) \
                - (self.end_x * data['beat_time'] / data['beat_time'] / 2)) \
                * self.size_x

            self.pos_cube.set_xyz(position_x, 0 , 0) # draw position



    def _end(self):
        self.parent_world.remove(self.world)


    def update(self, subject):
        status = subject.data['type']
        if status == 'roundStart':
            self._update_pos_bar(subject.data)
        elif status == 'activateNote':
            pass
        elif status == 'deActivateNote':
            pass
        elif status == 'nextLine':
            pass
        elif status == 'end':
            self._end()
        elif self.debug:
            print 'status: ',status

