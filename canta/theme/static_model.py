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
from canta.theme.rotating_body import RotatingBody

class StaticModel(Model):
    """Create a static (non-Cal3D) model.
    """

    def __init__(self, parent_world=None, name='', position=(0.0, 0.0, 0.0), \
            scale=(1.0, 1.0, 1.0), rotation=(0.0, 0.0, 0.0), shadow=False, \
            animation=False, cellshading=False, envmap=False, debug=False):

        self.debug = debug

        # call constructor of super class:
        Model.__init__(self, parent_world, name, position, scale, \
                rotation, self.debug)

        self.shadow = shadow
        self.animation = animation
        self.cellshading = cellshading
        self.envmap = envmap

        if self.cellshading:
            # create a cellshading model builder:
            model_builder = soya.CellShadingModelBuilder()

        else:
            # create a simple model builder:
            model_builder = soya.SimpleModelBuilder()

        # set the 'shadow' model_builder attribute:
        model_builder.shadow = self.shadow

        # create a world for the model:
        model_world = soya.World.get(self.name)

        if self.cellshading:
            #print 'CELLSHADING! Creating Material!'
            # modify the material for a better effect:
            #material = model_world.children[0].material
            #material.texture = soya.Image.get("grass.png")
            #material.separate_specular = 1
            #material.shininess = 15.0
            #material.specular = (1.0, 1.0, 1.0, 1.0)

            # creates the shader (a normal material with a texture):
            #shader = soya.Material()
            #shader.texture = soya.Image.get("shader.png")

            # Sets the model_builder properties. These properties can also be passed to the constructor,
            # see docstrings for more info.
            # The shader property is (obviously) the shader :-)
            # outline_color specifies the color of the outline (default : black)
            # outline_width specifies the width of the outline (default 4.0) ; set to 0.0 for no outline
            # outline_attenuation specifies how the distance affects the outline_width (default 0.3).
            #model_builder.shader              = shader
            model_builder.outline_color = (0.0, 0.0, 0.0, 1.0)
            model_builder.outline_width = 7.0
            model_builder.outline_attenuation = 1.0

        elif self.envmap:
            material = soya.Material()
            material.environment_mapping = True # Specifies environment mapping is active
            material.texture = soya.Image.get(self.envmap)# The textured sphere map

        # set the model_builder of the world:
        model_world.model_builder = model_builder

        if self.envmap:
            for face in model_world.children:
                face.smooth_lit=0
                face.material=material

        # create a model from the world:
        model = model_world.to_model()

        # create a body from the model:
        if self.animation is not None:
            self.body = RotatingBody(parent_world, model, rotation=self.animation)
        else:
            self.body = soya.Body(parent_world, model)

        # position, scale and rotate the body:
        self.set_position(self.position)
        self.set_scale(self.scale)
        self.set_rotation(self.rotation)

        # set name of the body:
        self.body.name = self.name

def main():
    pass

if __name__ == '__main__': main()

