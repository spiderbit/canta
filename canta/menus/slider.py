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

import soya, soya.pudding as pudding

class MenuSlider(pudding.control.Box):
    """A mouse dragable slider.
        * Takes a label, initial value, range and color scheme.
        TODO: write more stuff here.
    """

    def __init__(self, label, init_val, range, width, height, top, left, colors, debug = 0):

        self.debug = debug
        if self.debug: print 'DEBUG: Slider - init()'

        #pudding.control.Box.__init__(self, height = 22, width = 32, top = 144, left = 0)
        pudding.control.Box.__init__(self, height = height, width = width, top = top, left = left)
        self.label = label
        self.init_val = init_val
        self.pad = 4
        self.left = ((self.init_val) * range) + (range / 2) + self.pad
        self.left_limit = (self.width * 1.5)

        # tweak tweak (??):
        # TODO: What does he mean with "tweak tweak"?
        self.right_limit = (self.width * 1.5) + range + 1

        self.label.left = self.left + 6
        self.range = (self.right_limit - self.left_limit)
        self.val = self.init_val

        # minimal value:
        self.val_min = 0.01

        # maximal value:
        self.val_max = 0.99

        self.colors = colors
        self.border_color = self.colors.button_border

    def on_focus(self):
        if self.debug: print 'DEBUG: Slider - on_focus()'
        self.border_color = self.colors.button_border_on_focus

    def on_loose_focus(self):
        if self.debug: print 'DEBUG: Slider - on_loose_focus()'
        self.border_color = self.colors.button_border
        # commented this out, now it slides even if you loose focus:
        # TODO: lol, i was happy too soon.
        # it slides way over the edge if you move it fast.
        #soya.set_grab_input(0)

    def on_mouse_down(self, button, x, y):
        if self.debug: print 'DEBUG: Slider - on_mouse_down()'
        soya.set_grab_input(1)

    def on_mouse_up(self, button, x, y):
        if self.debug: print 'DEBUG: Slider - on_mouse_up()'
        soya.set_grab_input(0)

    def advance_time(self, proportion):

        mouse_pos_x = soya.get_mouse_rel_pos()[0]

        if self.left >= self.left_limit and self.left <= self.right_limit and soya.get_grab_input() == 1:

            # move slider puck to relative mouse pos:
            self.left += mouse_pos_x
            self.label.left = self.left + self.width / 4

            # find relative position of puck inside limits:
            relative_pos = self.range - (self.right_limit - self.left)

            # generate value from 0 - 1, round to three decimal places:
            self.val = round(relative_pos / (self.range), 3)

        elif self.val <= self.val_min:
            soya.set_grab_input(0)
            self.left = self.left_limit + 1
            # safe lower limit:
            self.val = 0.01

        elif self.val >= self.val_max:
            soya.set_grab_input(0)
            self.left = self.right_limit - 1
            self.val = .99

        elif soya.get_grab_input() == 0:
            self.left += 0 

        else:
            self.left += 0

        # update label value as a percentage each cycle:
        self.label.label = str(self.val * 100)[:-2]


if __name__ == '__main__':

    DEBUG = 1

    import soya, os
    import soya.sphere, soya.cube
    import soya.pudding.ext.fpslabel
    import Colors, Style

    # this argument is for the action function (?):
    arg = 'dummy'

    # this function is executed when you click the button:
    def action(arg):
        print 'action()'

    # init soya in resizable window:
    soya.init('Canta', 1024, 768, 0)

    # working dir:
    APP_DIR = os.path.join('..', os.curdir)

    # fonts:
    font = soya.Font(os.path.join(APP_DIR, 'data', 'fonts', 'DejaVuSansCondensed.ttf'), 16, 12)

    # global colors:
    colors = Colors.Colors(debug = DEBUG)

    # set soya's style path:
    style = Style.Style(APP_DIR, font, colors, DEBUG)

    # initialize pudding:
    pudding.init(style = style)

    # set the root scene:
    scene = soya.World()

    # create the pudding root widget:
    widget = pudding.core.RootWidget(width = 1024, height = 768)

    # a test filter:
    test_filter = .50

    # create a simple label for the slider:
    slider_label = pudding.control.SimpleLabel(
                    widget,
                    label = '50',
                    font = font,
                    top = 346,
                    left = 200,
                    z_index = 5
                    )

    
    slider = widget.add_child(Slider(
                    slider_label,
                    test_filter,
                    288,
                    colors,
                    DEBUG
                    ))

    # set up the camera:
    camera = soya.Camera(scene)
    camera.set_xyz(0.0, 0, 10.0)

    # set up the light:
    light = soya.Light(scene)
    light.set_xyz(1.0, 0.7, 1.0)

    # a test cube in the background:
    test_cube_world = soya.cube.Cube()
    test_cube_world.model_builder = soya.SolidModelBuilder()
    test_cube = soya.Body(scene, test_cube_world.to_model())
    test_cube.rotate_y(45.0)
    test_cube.rotate_x(45.0)

    # add the camera to the root widget:
    widget.add_child(camera)

    # set our root widget:
    soya.set_root_widget(widget)

    # add a FPS Label:
    pudding.ext.fpslabel.FPSLabel(soya.root_widget, position = pudding.BOTTOM_RIGHT)

    # start pudding main loop:
    pudding.main_loop.MainLoop(scene).idle()

