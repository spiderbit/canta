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

from soya import Smoke, FlagSubFire, FlagFirework, Particles
from canta.theme.rotating_body import RotatingBody

class CubeList:
    def __init__(self, parent_world):
        self.parent_world = parent_world
        self.world = soya.World()
        self.parent_world.add(self.world)


    def _delete_all(self):
        del self.world.children[0:]


    def draw_grid(self, words):
        # 12 balken + 13 falschbalken = 25 einheiten, jeder balken
        #10pixel hoch also insgesamt 250 pixel
        #resolution_y = 768.
        count_right_bar = self.max - self.min
        count_wrong_bar = count_right_bar + 1.
        #count_bar = count_right_bar + count_wrong_bar
        size_y = 0.2
        size_x = 0.3
        range_x = words[-1].timeStamp + words[-1].duration - words[0].timeStamp

        # create a new cube with the new coordinates:
        for i in range(count_right_bar):
            bar = soya.cube.Cube()
            bar.scale(size_x * range_x, size_y/10, 0.5)
            model = bar.to_model()
            # 2 ist für den abstand zwischen den noten
            position_y = ((i) - (count_right_bar / 2.) ) * size_y * 1
            position_x =  0 #( range_x -(range_x)/2 ) * 0.3
            if self.debug: print 'position: ', position_x

            #if i == pos:
            #	pos_z = 3

            #else:
            pos_z = 0
            x = soya.Body(self.world, model).set_xyz(position_x, position_y, pos_z)


    def add(self, properties):

        material = soya.Material()
        if properties['diffuse']:
            material.diffuse = properties['diffuse']

        #material.diffuse = (0.0, 0.2, 0.7, 1.0)
        # We use here a light blue, to get metallic reflexions.
        if properties['specular']:
            material.specular = properties['specular']

        # Activates the separate specular. This results in a brighter specular effect.
        if properties['seperate_specular']:
            material.separate_specular = 1



        self.use_pil = False
        self.use_shadows = False

        bar = soya.cube.Cube(material=material)
        bar.scale(self.size_x * properties['length'], self.size_y, 0.5)

        if self.use_pil:
            for face in bar.children:
                face.material = self.material

            model_builder = soya.SimpleModelBuilder()
            if self.use_shadows:
                model_builder.shadow = 1
            bar.model_builder = model_builder

        model = bar.to_model()

        if self.use_pil:
            self.material.environment_mapping = 1
            self.material.texture = soya.Image.get('env_map.jpeg')
        if properties['rotate']:
            body = RotatingBody(self.world, model)
        else:
            body = soya.Body(self.world, model)
        body.set_xyz(properties['x'], properties['y'], properties['z'])


    def _activate_note(self, pos):
        self.world.children[pos].z = 0.6


    def _de_activate_note(self, pos):
        self.world.children[pos].z = 0


    #def _bonus_draw(self, size_y, size_x, duration):
        #material = soya.Material()
        #material.diffuse = (1.0, 1.0, 1.0, 0.5)
        # We use here a blue diffuse color.


        # create a new cube with the new coordinates:
        #bar = soya.cube.Cube(material=material)
        #size_y = size_y * 2

        #fountain = FlagFirework(self.parent_world, nb_particles=4, nb_sub_particles=10)
        #bar.scale(size_x * duration, size_y, 0.5)
        #return bar.to_model()

    #def _freestyle_draw(self, size_y, size_x, duration):
        #material = soya.Material()
        #material.diffuse = (1.0, 0.2, 0.7, 1.0)
        #material.specular = (0.2, 0.0, 1.0, 1.0)
        #material.separate_specular = 1

        # create a new cube with the new coordinates:
        #bar = soya.cube.Cube(material=material)
        #size_y = size_y * 2

        #bar.scale(size_x * duration, size_y, 0.5)
        #return bar.to_model()


    def _end(self):
        self.parent_world.remove(self.world)

