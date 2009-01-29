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

class Panel(Model):
    """Display a rectangle with user-defined properties.
        Properties:
            * name
            * position
            * scale
            * rotation
            * color
            * texture
            * environment mapping
            * shadows
    """

    def __init__(self, parent_world, name='default', \
            position=(0., 0., 0.), scale=(1., 1., 1.),\
            rotation=(0., 0., 0.), color=None,
            texture=None, animation=None, shadow=False, debug=False):

        self.debug = debug

        Model.__init__(self, parent_world, name, position, \
                    scale, rotation)

        self.animation = animation
        self.color = color
        self.texture = texture
        self.environment_mapping = False
        self.shadow = shadow
        self.material = soya.Material()

        if self.texture:
            self.material.texture = soya.Image.get(self.texture)

        if self.color:
            self.material.diffuse = self.color

        if self.environment_mapping:
            self.material.environment_mapping = True

        # create a world for the model:
        world = soya.World()

        face = soya.Face(world, [
            soya.Vertex(world, 1.0, 1.0, 0.0, 1.0, 0.0),
            soya.Vertex(world, -1.0, 1.0, 0.0, 0.0, 0.0),
            soya.Vertex(world, -1.0, -1.0, 0.0, 0.0, 1.0),
            soya.Vertex(world, 1.0, -1.0, 0.0, 1.0, 1.0)
            ])

        # set the color of the face:
        face.material = self.material

        # set face double sided:
        face.double_sided = 1

        # create a model from the world:
        model = world.to_model()

        # create a body from the model:
        if self.animation is not None:
            self.body = RotatingBody(self.parent_world, model, rotation=self.animation)
        else:
            self.body = soya.Body(self.parent_world, model)

        # position, scale and rotate the body:
        self.set_position(self.position)
        self.set_scale(self.scale)
        self.set_rotation(self.rotation)

        # set name of the body:
        self.body.name = self.name

    def update_texture(self, texture):
        self.material.texture = soya.Image.get(texture)

if __name__ == '__main__':

    DEBUG = 1

    import sys
    import os
    import soya.cube

    # init soya in resizable window:
    soya.init('Canta', 1024, 768, 0)

    soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), '..', 'data'))

    # set the root scene:
    scene = soya.World()

    # create the test object:
    # the name:
    name = 'testpanel'
    # position, scale and rotation with (x, y, z):
    position = (0.0, 0.0, 1.0)
    scale = (5.0, 2.0, 5.0)
    rotation = (0.5, 0.5, 0.5)
    # color:
    color = (0.8, 0.4, 0.2, 0.7)

    # instanciate:
    test_guipanel = GuiPanel(
                scene,
                name,
                position,
                scale,
                rotation,
                color,
                DEBUG
                )

    # set up the camera:
    camera = soya.Camera(scene)
    camera.set_xyz(0.0, 0, 10.0)

    # set up the light:
    light = soya.Light(scene)
    light.set_xyz(0.0, 0.7, 1.0)

    # a test cube in the background:
    test_cube_world = soya.cube.Cube()
    test_cube_world.builder = soya.SolidModelBuilder()
    test_cube = soya.Body(scene, test_cube_world.to_model())
    test_cube.rotate_y(45.0)
    test_cube.rotate_x(45.0)
    test_cube.y = 2.3

    # a test atmosphere:
    #atmosphere = soya.SkyAtmosphere()
    #atmosphere.sky_color = (1, 1, 0.8, 1)
    #scene.atmosphere = atmosphere

    # set our root widget:
    soya.set_root_widget(camera)

    # start soya main loop:
    soya.MainLoop(scene).main_loop()

