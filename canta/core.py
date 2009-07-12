#! /usr/bin/python -O
# -*- coding: utf-8 -*-
#
#    CANTA - A free entertaining educational software for singing
#    Copyright (C) 2007, 2008  S. Huchler, A. Kattner, F. Lopez
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

import time
import sys
import os
import gettext
import user

import soya
import soya.pudding as pudding
import soya.pudding.ext.fpslabel
import soya.cube
import soya.sphere
import PIL.Image as pil
import soya.pudding.ext.slicingimage
import soya.pudding.listbox
from configobj import ConfigObj
from validate import Validator
import warnings

from canta.display.style import Style
from canta.theme.particle_system import ParticleSystem
from canta.directory import Directory
from canta.theme.theme_manager import ThemeManager
from canta.menus.main_menu import MainMenu


class Core:
    """Initialize
        * user configuration (screen resolution, fullscreen settings, selected theme, ...)
        * game engine
        * theme configuration (selected theme from XML)
        * widget system
        * all menus and needed instances.
        Then start the main loop.
    """
    def __init__(self, window_title='', app_dir = os.path.dirname(sys.argv[0])):

        self.app_dir = app_dir
        self.window_title = window_title
        self._start()


    def _start(self):

        # get user config settings and store them:
        self.config_path = os.path.join(user.home, '.canta')
        if not os.access(self.config_path, os.F_OK):
            os.mkdir(self.config_path)
        self.config = ConfigObj()
        vdt = Validator()
        # copy default config
        spec_file = os.path.join(self.app_dir, 'misc', 'configspec')
        self.config = ConfigObj(configspec=spec_file)
        print self.config.configspec.keys()
        self.config.filename = os.path.join(self.config_path, 'config')
        if not os.access(os.path.join(self.config_path, 'config'), os.F_OK):
            self.config.validate(vdt, copy=True)
            self.config.write()
        else:
            self.config = ConfigObj(os.path.join(self.config_path, 'config'), configspec=spec_file)
            self.config.validate(vdt)


        x, y =  self.config['screen']['resolution'].split('x')
        self.screen_res_x, self.screen_res_y = int (x), int(y)
        self.theme_name = self.config['theme']['name']


        self.widget_properties = {}
        self.widget_properties['theme'] = {}
        self.widget_properties['theme']['main'] = self.theme_name
        self.widget_properties['theme']['song'] = None

        self.widget_properties['config'] = self.config

        # initialize game engine:
        self._init_game_engine()


        ### CHRISTMAS TEST ###
        test = False
        if test:
            particles = ParticleSystem(self.root_world)
            particles.set_colors((1.0,1.0,1.0,1.0),(1.0,0.0,0.0,0.5), \
                (1.0,1.0,0.,0.5),(0.5,0.5,0.5,0.5),(0.,0.,0.,0.5))
            particles.set_sizes((0.19,0.19),(0.35,0.35))
            particles.set_xyz(10.0,-6.0,0.0)
            particles.rotate_z(-180.0)

        # load the theme config settings:
        self.theme_mgr = ThemeManager(self.root_world)
        self.theme_dir = os.path.join(self.app_dir, 'media', 'themes', self.theme_name)
        self.theme_mgr.get_theme(self.theme_name, self.theme_dir)

        self.widget_properties['font'] = {}

        font_elems = ['p', 'h1', 'lyrics', 'button']
        lyrics_types = ['to_sing', 'special', 'active', 'done']
        button_types = ['on_focus', 'off_focus']

        for elem in font_elems:
            self.widget_properties['font'][elem] = {}

        font_p = self.theme_mgr.get_font(self.theme_name, 'p', 'None', 'font')
        self.widget_properties['font']['p']['obj'] = font_p
        color_p = self.theme_mgr.get_font(self.theme_name, 'p', 'None', 'color')
        self.widget_properties['font']['p']['color'] = color_p

        font_h1 = self.theme_mgr.get_font(self.theme_name, 'h1', 'None', 'font')
        self.widget_properties['font']['h1']['obj'] = font_h1
        color_h1 = self.theme_mgr.get_font(self.theme_name, 'h1', 'None', 'color')
        self.widget_properties['font']['h1']['color'] = color_h1

        self.widget_properties['font']['lyrics']['to_sing'] = {}
        font_lyrics_ts = self.theme_mgr.get_font(self.theme_name, 'lyrics', 'to_sing', 'font')
        color_lyrics_ts = self.theme_mgr.get_font(self.theme_name, 'lyrics', 'to_sing', 'color')
        self.widget_properties['font']['lyrics']['to_sing']['obj'] = font_lyrics_ts
        self.widget_properties['font']['lyrics']['to_sing']['color'] = color_lyrics_ts

        self.widget_properties['font']['lyrics']['special'] = {}
        font_lyrics_spec = self.theme_mgr.get_font(self.theme_name, 'lyrics', 'special', 'font')
        color_lyrics_spec = self.theme_mgr.get_font(self.theme_name, 'lyrics', 'special', 'color')
        self.widget_properties['font']['lyrics']['special']['obj'] = font_lyrics_spec
        self.widget_properties['font']['lyrics']['special']['color'] = color_lyrics_spec

        self.widget_properties['font']['lyrics']['active'] = {}
        font_lyrics_act = self.theme_mgr.get_font(self.theme_name, 'lyrics', 'active', 'font')
        color_lyrics_act = self.theme_mgr.get_font(self.theme_name, 'lyrics', 'active', 'color')
        self.widget_properties['font']['lyrics']['active']['obj'] = font_lyrics_act
        self.widget_properties['font']['lyrics']['active']['color'] = color_lyrics_act

        self.widget_properties['font']['lyrics']['done'] = {}
        font_lyrics_done = self.theme_mgr.get_font(self.theme_name, 'lyrics', 'done', 'font')
        color_lyrics_done = self.theme_mgr.get_font(self.theme_name, 'lyrics', 'done', 'color')
        self.widget_properties['font']['lyrics']['done']['obj'] = font_lyrics_done
        self.widget_properties['font']['lyrics']['done']['color'] = color_lyrics_done

        self.widget_properties['font']['button']['on_focus'] = {}
        font_button_on = self.theme_mgr.get_font(self.theme_name, 'button', 'on_focus', 'font')
        color_button_on = self.theme_mgr.get_font(self.theme_name, 'button', 'on_focus', 'color')
        self.widget_properties['font']['button']['on_focus']['obj'] = font_button_on
        self.widget_properties['font']['button']['on_focus']['color'] = color_button_on

        self.widget_properties['font']['button']['off_focus'] = {}
        font_button_off = self.theme_mgr.get_font(self.theme_name, 'button', 'off_focus', 'font')
        color_button_off = self.theme_mgr.get_font(self.theme_name, 'button', 'off_focus', 'color')
        self.widget_properties['font']['button']['off_focus']['obj'] = font_button_off
        self.widget_properties['font']['button']['off_focus']['color'] = color_button_off

        self.widget_properties['box'] = self.theme_mgr.get_box(self.theme_name)
        self.widget_properties['button'] = self.theme_mgr.get_button(self.theme_name)

        self.widget_properties['bar'] = self.theme_mgr.get_bar(self.theme_name)

        # initialize widget system:
        self._init_widget_engine()

        # show selected theme:
        self.theme_mgr.show_theme(self.theme_name)

        # Init menus and instances:
        self.init_menus()


    def init_menus(self):
        """Initialize all menus, then tell pudding main loop to idle().
        """

#       self.menus = {}

        # Main menu:

        main_menu = MainMenu(self.widget_properties, self.config, \
            self.theme_mgr, self.camera, core=self)
        main_menu.visible=1
        pudding.main_loop.MainLoop(self.root_world).idle()



    def _init_game_engine(self):
        """Initialize soya game engine, append our paths to soya's paths,
            create the scene and set up a camera.
        """

        # Hide window manager's resizability
        # features (maximise, resize, ...):
        RESIZEABLE = False

        soya.init(title=self.window_title, \
                width=self.screen_res_x,
                height=self.screen_res_y, \
                fullscreen=int(self.config['screen'].as_bool('fullscreen')), \
                resizeable=RESIZEABLE, sound=False)

        # Enable/disable soya's auto (blender model) importer:
        soya.AUTO_EXPORTERS_ENABLED = True

        # Append some paths:
        #	* themes/[selected theme name]/media
        #	TODO: append paths for all themes in themes/,
        #	so we can change the theme at runtime (?)...
        #	* songs/[song name]/media
        default_path = os.path.join(self.app_dir, 'media', 'themes', \
            'default', 'media')
        soya.path.append(default_path)
        theme_path = os.path.join(self.app_dir, 'media', 'themes', \
            self.widget_properties['theme']['main'], 'media')
        soya.path.append(theme_path)

        self.root_world = soya.World()
        self.widget_properties['root_world'] = self.root_world
        # set up a camera:
        self.camera = soya.Camera(self.root_world)

        ### CAMERA TESTS ###
        moveable = False
        rotating = False
        if moveable:
            from lib.cameras.movable_camera import MovableCamera
            self.camera = MovableCamera(self.app_dir, self.parent_world)
        if rotating:
            from lib.cameras.spinning_camera import SpinningCamera
            cube = soya.Body(self.root_world, soya.cube.Cube().to_model())
            cube.visible = 0
            self.camera = SpinningCamera(self.root_world, cube)
        ### END CAMERA TESTS ###

        self.camera.set_xyz(0.0, 0.0, 15.0)

        self.light = soya.Light(self.root_world)
        self.light.set_xyz(0.0, 7.7, 17.0)

    def _init_widget_engine(self):
        """Initialize the pudding widget system, create a root widget.
        """
        pudding.init(style=Style(self.widget_properties))

        # Create a pudding root widget:
        self.root_widget = pudding.core.RootWidget( \
                width=self.screen_res_x,
                height=self.screen_res_y, \
                top=0, left=0)

        self.widget_properties['root_widget'] = self.root_widget

        self.root_widget.add_child(self.camera)
        soya.set_root_widget(self.root_widget)
        pudding.main_loop.MainLoop(self.root_world).update()



def main():
    pass

if __name__ == '__main__': main()

