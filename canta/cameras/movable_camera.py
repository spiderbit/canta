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
import soya.sdlconst
import time

class MovableCamera(soya.Camera):
    """A keyboard-controlled camera and a rendering loop.
        * window resizing(!)
        * Buttons are:
        ** Arrow up: Move forward
        ** Arrow down: Move backward
        ** Arrow left: Turn left
        ** Arrow right: Turn right
        ** o: look up
        ** k: look down
        ** t: toggle wireframe
        ** r: screenshot
        ** ESC key: Quit
        ** q key: Quit
    """

    def __init__(self, app_dir='.', parent_world=None, debug=False):
        soya.Camera.__init__(self, parent_world)
        self.debug = debug
        self.app_dir = app_dir

        self.speed = soya.Vector(self)
        self.rotation_y_speed = 0.0
        self.rotation_x_speed = 0.0

    def begin_roundzz(self):
        soya.Camera.begin_round(self)

        # go through the events:
        for event in soya.process_event():
            # key pressed:
            if event[0] == soya.sdlconst.KEYDOWN:
                #print self.x, self.y, self.z
                # [ARROW UP] - move forward:
                if event[1] == soya.sdlconst.K_UP or event[1] == soya.sdlconst.K_w:
                    if self.debug: print 'DEBUG: MovableCamera - key pressed - [ARROW UP]'
                    self.speed.z = -0.2
                # [ARROW DOWN] - move backward:
                elif event[1] == soya.sdlconst.K_DOWN or event[1] == soya.sdlconst.K_s:
                    if self.debug: print 'DEBUG: MovableCamera - key pressed - [ARROW DOWN]'
                    self.speed.z =  0.2
                # [ARROW LEFT] - turn left:
                elif event[1] == soya.sdlconst.K_LEFT or event[1] == soya.sdlconst.K_a:
                    if self.debug: print 'DEBUG: MovableCamera - key pressed - [ARROW LEFT]'
                    self.rotation_y_speed =  1.5
                # [ARROW RIGHT] - turn right:
                elif event[1] == soya.sdlconst.K_RIGHT or event[1] == soya.sdlconst.K_d:
                    if self.debug: print 'DEBUG: MovableCamera - key pressed - [ARROW RIGHT]'
                    self.rotation_y_speed = -1.5
                # [s] - take a screenshot:
                elif event[1] == soya.sdlconst.K_s:
                    if self.debug: print 'DEBUG: UserInputManager - key pressed - [s]'
                    self.make_screenshot()
                # [t] - toggle wireframe:
                elif event[1] == soya.sdlconst.K_t:
                    if self.debug: print 'DEBUG: UserInputManager - key pressed - [t]'
                    soya.toggle_wireframe()
                # [q] - quit:
                elif event[1] == soya.sdlconst.K_q:
                    if self.debug: print 'DEBUG: MovableCamera - key pressed - [q]'
                    soya.MAIN_LOOP.stop()
                # [ESC] - quit:
                elif event[1] == soya.sdlconst.K_ESCAPE:
                    if self.debug: print 'DEBUG: MovableCamera - key pressed - [ESCAPE]'
                    soya.MAIN_LOOP.stop()
                # [o] - look up:
                elif event[1] == soya.sdlconst.K_o:
                    if self.debug: print 'DEBUG: MovableCamera - key pressed - [o]'
                    self.rotation_x_speed = 1.0
                # [k] - look down:
                elif event[1] == soya.sdlconst.K_k:
                    if self.debug: print 'DEBUG: MovableCamera - key pressed - [k]'
                    self.rotation_x_speed = -1.0
                # [k] - look down:
                elif event[1] == soya.sdlconst.K_r:
                    if self.debug: print 'DEBUG: MovableCamera - key pressed - [r]'
                    self.make_screenshot()

            # key released:
            if event[0] == soya.sdlconst.KEYUP:
                # [ARROW UP] - stop motion:
                if event[1] == soya.sdlconst.K_UP or event[1] == soya.sdlconst.K_w:
                    self.speed.z = 0.0
                # [ARROW DOWN] - stop motion:
                elif event[1] == soya.sdlconst.K_DOWN or event[1] == soya.sdlconst.K_s:
                    self.speed.z = 0.0
                # [ARROW LEFT] - stop motion:
                elif event[1] == soya.sdlconst.K_LEFT or event[1] == soya.sdlconst.K_a:
                    self.rotation_y_speed = 0.0
                # [ARROW RIGHT] - stop motion:
                elif event[1] == soya.sdlconst.K_RIGHT or event[1] == soya.sdlconst.K_d:
                    self.rotation_y_speed = 0.0
                # [o] - look up:
                elif event[1] == soya.sdlconst.K_o:
                    self.rotation_x_speed = 0.0
                # [k] - look down:
                elif event[1] == soya.sdlconst.K_k:
                    self.rotation_x_speed = 0.0

            # Mouse motion moves the dragdroping object, if there is one.
            #if event[0] == soya.sdlconst.MOUSEMOTION:
            #	self.prev_coords = self.coord2d_to_3d(event[1], event[2])
            #	coords = self.coord2d_to_3d(event[1], event[2], event[3])
            #	print coords


    def advance_time(self, proportion):
        self.add_mul_vector(proportion, self.speed)
        self.turn_y(self.rotation_y_speed * proportion)
        self.turn_x(self.rotation_x_speed * proportion)

    def make_screenshot(self):
        """Take a screenshot and save it to data/screenshots.
        """
        soya.screenshot().save(os.path.join(self.app_dir, 'canta_' \
            + str(time.strftime('%S' +'%H'+'%M'+'_'+'%d'+'-'+'%h'+'-'+'%Y')) \
            + '.jpeg'))

def main():
    DEBUG = 1

    import sys
    import os
    import soya.cube

    # init soya in resizable window:
    soya.init('MovableCamera Module', 1024, 768, 0)
    soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), '..', '..', 'media', 'themes', 'kiddy', 'media'))
    # set the root scene:
    scene = soya.World()

    # set up the light:
    light = soya.Light(scene)
    light.set_xyz(0.0, 0.7, 1.0)

    # set up the camera:
    camera = MovableCamera(app_dir = '.', parent_world = scene, debug = DEBUG)
    camera.set_xyz(0.0, 0, 10.0)

    # a test cube in the background:
    test_cube_world = soya.cube.Cube()
    test_cube_world.model_builder = soya.SolidModelBuilder()
    test_cube = soya.Body(scene, test_cube_world.to_model())
    test_cube.rotate_y(45.0)
    test_cube.rotate_x(45.0)

    atmosphere = soya.SkyAtmosphere()
    atmosphere.bg_color = (1.0, 0.0, 0.0, 1.0)
    atmosphere.ambient = (0.5, 0.5, 0.0, 1.0)
    atmosphere.skyplane = 1
    atmosphere.sky_color = (1.0, 1.0, 0.0, 1.0)
    atmosphere.cloud = soya.Material(soya.Image.get('cloud.png'))

    scene.atmosphere = atmosphere
    # set our root widget:
    soya.set_root_widget(camera)

    # start soya main loop:
    soya.MainLoop(scene).main_loop()

if __name__ == '__main__': main()
