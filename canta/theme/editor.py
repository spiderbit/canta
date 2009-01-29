#! /usr/bin/python -O
# -*- coding: utf-8 -*-
#
#    CANTA Theme Editor - An editor for themes used in CANTA
#    Copyright (C) 2008  A. Kattner
#    Soya 3D tutorial
#    Copyright (C) 2004 Jean-Baptiste LAMY
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
import soya.cube
import soya.sphere
import soya.sdlconst

# Soya provides 2 raypicking functions: raypick and raypick_b ("b" stands for boolean).
# The first version returns a (IMPACT, NORMAL) tuple. IMPACT is the impact Point, and
# IMPACT.parent is the object hit. NORMAL is the normal Vector of the object at the
# impact (usefull e.g. for reflection).
# The boolean version simply returns true if something is hit.

# Both take the same arguments:
# - ORIGIN:    the origin of the ray (a Position)
# - DIRECTION: the direction of the ray (a Vector)
# - DISTANCE:  the maximum distance of the ray; -1.0 (default) for no distance limit
# - HALF_LINE: if true (default), the ray goes only in the direction of DIRECTION.
#              if false, the ray goes both in DIRECTION and -DIRECTION, and so can hit
#              objects backward.
# - CULL_FACE  if true (default), does not take into account invisible sides of non-double
#              sided faces (Face.double_sided = 0).

# For speeding up, raypick has 2 optional arguments, a Point and a Vector. If given,
# these Point and Vector will be returned in the tuple, instead of creating new objects.

class Editor(soya.World):
    def __init__(self, parent, cam):
        soya.World.__init__(self, parent)

        # The object we are currently dragdroping (None => no dragdrop).
        self.dragdroping = None

        # The impact point
        self.impact = None

        self.speed = soya.Vector(self)
        self.rotation_y_speed = 0.0
        self.rotation_x_speed = 0.0

        self.cam = cam
        self.point = soya.Point(parent)
        self.point.set_xyz(0,0,0)
        self.debug = False

    def begin_round(self):
        soya.World.begin_round(self)

        for event in soya.process_event():
            
            # Mouse down initiates the dragdrop.
                        # key pressed:
            if event[0] == soya.sdlconst.KEYDOWN:
                #print self.x, self.y, self.z
                # [ARROW UP] - move forward:
                if event[1] == soya.sdlconst.K_UP or event[1] == soya.sdlconst.K_w:
                    self.cam.speed.z = -0.2
                # [ARROW DOWN] - move backward:
                elif event[1] == soya.sdlconst.K_DOWN or event[1] == soya.sdlconst.K_s:
                    self.cam.speed.z = 0.2
                # [ARROW LEFT] - turn left:
                elif event[1] == soya.sdlconst.K_LEFT or event[1] == soya.sdlconst.K_a:
                    self.cam.rotation_y_speed = 1.5
                # [ARROW RIGHT] - turn right:
                elif event[1] == soya.sdlconst.K_RIGHT or event[1] == soya.sdlconst.K_d:
                    self.cam.rotation_y_speed = -1.5
                # [s] - take a screenshot:
                #elif event[1] == soya.sdlconst.K_s:
                #	self.make_screenshot()
                # [b] - toggle wireframe:
                elif event[1] == soya.sdlconst.K_b:
                    soya.toggle_wireframe()
                # [q] - quit:
                #elif event[1] == soya.sdlconst.K_q:
                #	soya.MAIN_LOOP.stop()
                # [ESC] - quit:
                elif event[1] == soya.sdlconst.K_ESCAPE:
                    soya.MAIN_LOOP.stop()
                # [p] - look up:
                elif event[1] == soya.sdlconst.K_p:
                    self.cam.rotation_x_speed = 1.0
                # [l] - look down:
                elif event[1] == soya.sdlconst.K_l:
                    self.cam.rotation_x_speed = -1.0
                #TODO:  [x] - save world:
                #elif event[1] == soya.sdlconst.K_x:
                #	self.save()
                # [e] - rotate world:
                elif event[1] == soya.sdlconst.K_e:
                    self.rotation_y_speed = 1.5
                # [r] - rotate world:
                elif event[1] == soya.sdlconst.K_r:
                    self.rotation_y_speed = -1.5
                # [u] - reset camera position:
                elif event[1] == soya.sdlconst.K_u:
                    self.cam.set_xyz(0.0, 0.0, 15.0)
                    self.cam.look_at_y(self.point)
                # [o] - rotate world:
                elif event[1] == soya.sdlconst.K_o:
                    self.rotation_x_speed = 1.5
                # [k] - rotate world:
                elif event[1] == soya.sdlconst.K_k:
                    self.rotation_x_speed = -1.5

            # key released:
            elif event[0] == soya.sdlconst.KEYUP:
                # [ARROW UP] - stop motion:
                if event[1] == soya.sdlconst.K_UP or event[1] == soya.sdlconst.K_w:
                    self.cam.speed.z = 0.0
                # [ARROW DOWN] - stop motion:
                elif event[1] == soya.sdlconst.K_DOWN or event[1] == soya.sdlconst.K_s:
                    self.cam.speed.z = 0.0
                # [ARROW LEFT] - stop motion:
                elif event[1] == soya.sdlconst.K_LEFT or event[1] == soya.sdlconst.K_a:
                    self.cam.rotation_y_speed = 0.0
                # [ARROW RIGHT] - stop motion:
                elif event[1] == soya.sdlconst.K_RIGHT or event[1] == soya.sdlconst.K_d:
                    self.cam.rotation_y_speed = 0.0
                # [p] - stop looking up:
                elif event[1] == soya.sdlconst.K_p or event[1] == soya.sdlconst.K_l:
                    self.cam.rotation_x_speed = 0.0
                elif event[1] == soya.sdlconst.K_e or event[1] == soya.sdlconst.K_r:
                    self.rotation_y_speed = 0.0
                # [o/k] - stop rotate world:
                elif event[1] == soya.sdlconst.K_o or event[1] == soya.sdlconst.K_k:
                    self.rotation_x_speed = 0.0

            elif event[0] == soya.sdlconst.MOUSEBUTTONDOWN:
                # The event give us the 2D mouse coordinates in pixel. The camera.coord2d_to_3d
                # convert these 2D pixel coordinates into a soy.Point object.
                mouse = self.cam.coord2d_to_3d(event[2], event[3])

                # Performs a raypicking, starting at the camera and going toward the mouse.
                # The vector_to method returns the vector between 2 positions.
                # This raypicking grabs anything that is under the mouse. Raypicking returns
                # None if nothing is encountered, or a (impact, normal) tuple, where impact is the
                # position of the impact and normal is the normal vector at this position.
                # The object encountered is impact.parent ; here, we don't need the normal.
                result = self.raypick(self.cam, self.cam.vector_to(mouse))
                if result:
                    self.impact, normal = result
                    self.dragdroping = self.impact.parent

                    # Converts impact into the camera coordinate system, in order to get its Z value.
                    # camera.coord2d_to_3d cannot choose a Z value for you, so you need to pass it
                    # as a third argument (it defaults to -1.0). Then, we computes the old mouse
                    # position, which has the same Z value than impact.
                    self.impact.convert_to(self.cam)
                    self.old_mouse = self.cam.coord2d_to_3d(event[2], event[3], self.impact.z)


            # Mouse up ends the dragdrop.
            elif event[0] == soya.sdlconst.MOUSEBUTTONUP:
                self.dragdroping = None

            # Mouse motion moves the dragdroping object, if there is one.
            elif event[0] == soya.sdlconst.MOUSEMOTION:
                if self.dragdroping:

                    # Computes the new mouse position, at the same Z value than impact.
                    new_mouse = self.cam.coord2d_to_3d(event[1], event[2], self.impact.z)

                    # Translates dragdroping by a vector starting at old_mouse and ending at
                    # new_mouse.
                    self.dragdroping.add_vector(self.old_mouse.vector_to(new_mouse))

                    # Store the current mouse position.
                    self.old_mouse = new_mouse


    def save(self):
        self.filename = 'theme'
        self.save()


    def advance_time(self, proportion):
        soya.World.advance_time(self, proportion)
        self.add_mul_vector(proportion, self.speed)
        self.turn_y(self.rotation_y_speed * proportion)
        self.turn_x(self.rotation_x_speed * proportion)



def main():
    soya.init()
    #soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))

    # Creates the scene.
    scene = soya.World()

    # Creates a camera.
    camera = soya.Camera(scene)
    camera.set_xyz(0.0, 0.0, 4.0)
    camera.fov = 100.0

    # Creates a dragdrop world.
    world = Editor(scene, camera)

    # Adds some bodys with different models, at different positions.
    red   = soya.Material(); red  .diffuse = (1.0, 0.0, 0.0, 1.0)
    green = soya.Material(); green.diffuse = (0.0, 1.0, 0.0, 1.0)
    blue  = soya.Material(); blue .diffuse = (0.0, 0.0, 1.0, 1.0)

    soya.Body(world, soya.cube.Cube(None, red  ).to_model()).set_xyz(-1.0, -1.0, 1.0)
    soya.Body(world, soya.cube.Cube(None, green).to_model()).set_xyz( 0.0, -1.0, 0.0)
    soya.Body(world, soya.cube.Cube(None, blue ).to_model()).set_xyz( 1.0, -1.0, -1.0)

    soya.Body(world, soya.sphere.Sphere().to_model()).set_xyz(1.0, 1.0, 0.0)

    # Adds a light.
    light = soya.Light(scene)
    light.set_xyz(0.0, 0.2, 1.0)

    soya.set_root_widget(camera)

    # Main loop

    soya.MainLoop(scene).main_loop()


if __name__ == '__main__': main()

