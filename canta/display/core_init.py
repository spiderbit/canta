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
from canta.display.properties import DisplayProperties
from canta.theme.theme_manager import ThemeManager
from canta.menus.song_editor_browser import SongEditorBrowser
from canta.menus.song_browser import SongBrowser
from canta.menus.menu import Menu
from canta.menus.button import MenuButton
from canta.menus.item_group import MenuGroup
from canta.menus.browser import MenuBrowser
from canta.menus.text import MenuText
from canta.song.song_editor import SongEditor
from canta.display.sing_screen import SingScreen

from canta.song.midi_editor import MidiEditor
from canta.song import song_loader

from canta.theme.particle_system import ParticleSystem
from canta.display.language import LocaleManager



class CoreInit:
    """Initialize
        * user configuration (screen resolution, fullscreen settings, selected theme, ...)
        * game engine
        * theme configuration (selected theme from XML)
        * widget system
        * all menus and needed instances.
        Then start the main loop.
    """
    def __init__(self, window_title='', app_dir = os.path.dirname(sys.argv[0]), debug=0):

        self.app_dir = app_dir
        self.debug = debug
        self.window_title = window_title
        self._start()


    def check_sound_modules(self):
        try:
             import pygame, Numeric
        except ImportError:
             self.valid_sound_players.remove('PyGame')
        try:
             import oss, numpy
        except ImportError:
             self.valid_sound_inputs.remove('OSS')
        try:
             import pyaudio, numpy
        except ImportError:
             self.valid_sound_inputs.remove('PyAudio')


    def _start(self):

        self.valid_sound_players = ['PyGame', 'Dummy', 'Gstreamer']
        self.valid_sound_inputs = ['OSS', 'PyAudio', 'Gstreamer']
        self.check_sound_modules()

        # get user config settings and store them:
        self.config_path = os.path.join(user.home, '.canta')
        if not os.access(self.config_path, os.F_OK):
            os.mkdir(self.config_path)
        self.config = ConfigObj()
        vdt = Validator()
        # copy default config
        spec_file = os.path.join(self.app_dir,'configspec')
        self.config = ConfigObj(configspec=spec_file)
        self.config.filename = os.path.join(self.config_path, 'config')
        if not os.access(os.path.join(self.config_path, 'config'), os.F_OK):
            self.config.validate(vdt, copy=True)
            self.config.write()
        else:
            self.config = ConfigObj(os.path.join(self.config_path, 'config'), configspec=spec_file)
            self.config.validate(vdt)

        self.locale = self.config['misc']['locale']
        self.octave = int(self.config['misc'].as_bool('octave'))

        self.screen_res_x =  self.config['screen'].as_int('resolution_x')
        self.screen_res_y =  self.config['screen'].as_int('resolution_y')
        self.fullscreen_on = int(self.config['screen'].as_bool('fullscreen'))
        self.fps_label = int(self.config['screen'].as_bool('fps_label'))
        self.use_pil = int(self.config['screen'].as_bool('pil'))
        self.sound_player = self.config['sound']['player']
        self.sound_input = self.config['sound']['input']
        self.sound_preview = int(self.config['sound'].as_bool('preview'))
        self.theme_name = self.config['theme']['name']

        self.widget_properties = {}
        self.widget_properties['theme'] = {}
        self.widget_properties['theme']['main'] = self.theme_name
        self.widget_properties['theme']['song'] = None

        self.widget_properties['config'] = self.config

        self.lm = LocaleManager(self.app_dir)
        self.lm.install(self.locale)

        self.disp = DisplayProperties()

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
        self.theme_mgr = ThemeManager(self.root_world, self.debug)
        self.theme_dir = os.path.join(self.app_dir, 'themes', self.theme_name)
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


    def _init_game_engine(self):
        """Initialize soya game engine, append our paths to soya's paths,
            create the scene and set up a camera.
        """

        # Hide window manager's resizability
        # features (maximise, resize, ...):
        RESIZEABLE = False

        soya.init(title=self.window_title, \
                width=self.screen_res_x, height=self.screen_res_y, \
                fullscreen=self.fullscreen_on, \
                resizeable=RESIZEABLE, sound=False)

        # Enable/disable soya's auto (blender model) importer:
        soya.AUTO_EXPORTERS_ENABLED = True

        # Append some paths:
        #	* themes/[selected theme name]/media
        #	TODO: append paths for all themes in themes/,
        #	so we can change the theme at runtime (?)...
        #	* songs/[song name]/media
        default_path = os.path.join(self.app_dir, 'themes', \
            'default', 'media')
        soya.path.append(default_path)
        theme_path = os.path.join(self.app_dir, 'themes', \
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
            self.camera = MovableCamera(self.app_dir, self.parent_world, debug=self.debug)
        if rotating:
            from lib.cameras.spinning_camera import SpinningCamera
            cube = soya.Body(self.root_world, soya.cube.Cube().to_model())
            cube.visible = 0
            self.camera = SpinningCamera(self.root_world, cube)
        ### END CAMERA TESTS ###

        self.camera.set_xyz(0.0, 0.0, 15.0)

        self.light = soya.Light(self.root_world)
        self.light.set_xyz(0.0, 7.7, 17.0)


    def load_player(self):
        # The music players:
        if self.sound_player == 'Dummy':
            from canta.player.dummy_player import DummyPlayer
            self.player = DummyPlayer()
        elif self.sound_player == 'Gstreamer':
            from canta.player.gst_player import GSTPlayer
            self.player = GSTPlayer()
        elif self.sound_player == 'PyGame':
            from canta.player.pygame_player import PygamePlayer
            self.player = PygamePlayer()
        else:
            print "something wrong in configfile, player not found!"
            sys.exit(0)

    def _init_widget_engine(self):
        """Initialize the pudding widget system, create a root widget.
        """
        pudding.init(style=Style(self.widget_properties, self.debug))

        # Create a pudding root widget:
        self.root_widget = pudding.core.RootWidget( \
                width=self.screen_res_x, \
                height=self.screen_res_y, \
                top=0, left=0)

        self.widget_properties['root_widget'] = self.root_widget

        # Loading Label:
        # This should come immediatly, but it comes too late (after
        # the models are loaded).
        lc_top = self.screen_res_x / 2
        lc_left = self.screen_res_x / 2 - 100
        self.loading_cont = pudding.container.HorizontalContainer( \
                self.root_widget, \
                top=lc_top,
                left=lc_left,
                width=10, height=10, z_index=1)
        self.loading_cont.anchors = pudding.ANCHOR_RIGHT \
                     | pudding.ANCHOR_TOP | \
                    pudding.ANCHOR_LEFT
        self.loading_cont.add_child(pudding.control.SimpleLabel(
                    label=_(u'Loading, please wait...'),
                    font=self.widget_properties['font']['p']['obj'],
                    top=10,
                    left=10,
                    color=self.widget_properties['font']['p']['color']
                    ), pudding.EXPAND_HORIZ)

        self.root_widget.add_child(self.camera)
        soya.set_root_widget(self.root_widget)

        if self.fps_label:
            pudding.ext.fpslabel.FPSLabel(soya.root_widget, \
                position = pudding.TOP_RIGHT)

        pudding.main_loop.MainLoop(self.root_world).update()


    def init_menus(self):
        """Initialize all menus, then tell pudding main loop to idle().
        """

        # Button labels:
        l_start = _(u"Sing")#_(u'Party Mode')
        l_song_editor = _(u'Song Editor')
        #l_midi_editor = _(u'MIDI Editor')
        l_settings_main = _(u'Settings')
        l_settings_screen = _(u'Screen')
        l_settings_sound = _(u'Sound')
        l_settings_theme = _(u'Theme')
        l_settings_misc = _(u'Misc')
        l_about = _(u'About')
        l_quit2 = _(u'Quit')

        l_back =  _(u'back')
        l_save =  _(u'save')
        l_save_quit =  _(u'save & restart')
        l_quit =  _(u'quit')

        # Menu headings:
        h1_main_menu =  _(u'Main Menu')
        h1_settings_main =  _(u'Settings')
        h1_settings_screen =  _(u'Screen Settings')
        h2_settings_screen =  _(u'SCREEN:')
        h1_settings_sound =  _(u'Sound Settings')
        h2_settings_sound =  _(u'SOUND:')
        h1_settings_theme =  _(u'Theme Settings')
        h2_settings_theme =  _(u'THEME:')
        h1_settings_misc = _(u'Miscellaneous Settings')
        h2_settings_misc = _(u'Miscellaneous')
        h1_about =  _(u'About')
        h1_song_browser =  _(u'Choose a song...')

        # Settings:
        valid_languages = self.lm.get_langs()
        on_off_toggle = [('off'), ('on')]
        i_resolution =  _(u'Resolution:')
        i_fullscreen =  _(u'Fullscreen:')
        i_fps_label =  _(u'FPS label:')
        i_pil =  _(u'Cover images:')
        i_sound_output =  _(u'Select sound output engine:')
        i_sound_input =  _(u'Select sound input engine:')
        i_song_preview =  _(u'Play preview in song browser (experimental):')
        i_theme =  _(u'Choose a theme:')
        i_lan = _(u'Choose a language:')
        i_octave = _(u'Octave correctness:')

        # File paths:
        about_file = 'ABOUT.txt'
        logo_path = 'logo.png'
        show_logo = False

        # obsolete?
        self.menus = {}

        # Main menu:
        main_menu = Menu(self.widget_properties)
        main_menu.set_heading(h1_main_menu)
        self.menus['main'] = main_menu # obsolete?

        # About menu:
        about_menu = MenuText(self.widget_properties, top=self.screen_res_y / 3, \
                left=self.screen_res_x / 2)
        about_menu.set_heading(h1_about)
        about_menu.set_bg_box()
        about_back = MenuButton(l_back, widget_properties = self.widget_properties, target = main_menu)
        about_menu.add(about_back, 'horiz')
        about_quit = MenuButton(l_quit, function=self.quit, pos_size=0, widget_properties = self.widget_properties)
        about_menu.add(about_quit, 'center')
        fd_license = open(os.path.join(self.app_dir, about_file), 'r')
        license = fd_license.read()
        about_menu.add_text(license)

        # Song browser:
        song_objects = song_loader.search_songs(os.path.join(self.app_dir, 'songs'))
        song_objects_home = song_loader.search_songs(os.path.join(self.config_path, 'songs'))
        song_objects.extend(song_objects_home)

        self.load_player()

        # Song editor:'theme_mgr'
        song_editor = SongEditor(self.app_dir, self.widget_properties, \
            self.theme_mgr, main_menu, player=self.player, debug=self.debug )



        song_editor_browser = SongEditorBrowser(song_objects_home, \
            self.widget_properties, self.use_pil, self.sound_preview, player = self.player, start_screen=song_editor)
        song_editor_browser.set_heading(h1_song_browser)
        song_editor_browser.set_bg_box()
        self.menus['browser_editor'] = song_editor_browser

        back_button = MenuButton(l_back,  widget_properties=self.widget_properties, target=main_menu, function=song_editor_browser.stop_preview)
        quit_button = MenuButton(l_quit, function=self.quit, pos_size=0, widget_properties=self.widget_properties)
        song_editor_browser.add(back_button, 'center')
        song_editor_browser.add(quit_button, 'center')



        # Sing screen:
        sing_screen = SingScreen(app_dir=self.app_dir, \
                    camera=self.camera, theme_mgr=self.theme_mgr, \
                    widget_properties=self.widget_properties, \
                    menu_list=self.menus, config=self.config, \
                    octave=self.octave, player=self.player,debug=self.debug)

        song_browser = SongBrowser(song_objects, \
            self.widget_properties, self.use_pil, \
            self.sound_preview, self.octave, start_screen=sing_screen, \
            player=self.player)

        song_browser.set_heading(h1_song_browser)
        song_browser.set_bg_box()
        self.menus['browser'] = song_browser

        sb_back = MenuButton(l_back, target=main_menu, widget_properties = self.widget_properties,function=song_browser.stop_preview)
        sb_quit = MenuButton(l_quit, function=self.quit, pos_size=0, widget_properties = self.widget_properties)
        song_browser.add(sb_back, 'center')
        song_browser.add(sb_quit, 'center')


        # Options parent menu:
        self.options_menu_main = Menu(self.widget_properties)
        self.options_menu_main.set_heading(h1_settings_main)
        self.options_menu_main.set_bg_box()

        # Options sub menus:
        self.options_menu_screen = MenuGroup(self.widget_properties)
        self.options_menu_screen.set_heading(h1_settings_screen)
        self.options_menu_sound = MenuGroup(self.widget_properties)
        self.options_menu_sound.set_heading(h1_settings_sound)
        self.options_menu_theme = MenuGroup(self.widget_properties)
        self.options_menu_theme.set_heading(h1_settings_theme)
        self.options_menu_misc = MenuGroup(self.widget_properties)
        self.options_menu_misc.set_heading(h1_settings_misc)

        pos_size = {}
        pos_size['height'] = self.screen_res_y / 16
        pos_size['width'] = self.screen_res_x - 80
        pos_size['top'] = 10
        pos_size['left'] = 10

        # Add buttons to options parent menu:
        self.options_menu_main.add(MenuButton(l_back, target=main_menu, \
            widget_properties=self.widget_properties, pos_size=pos_size), 'horiz')
        self.options_menu_main.add(MenuButton(l_save, function=self.save, \
            widget_properties = self.widget_properties, pos_size=pos_size), 'horiz')
        self.options_menu_main.add(MenuButton(l_save_quit, function=self.save, \
            args='quit', widget_properties=self.widget_properties, pos_size=pos_size), 'horiz')

        self.options_menu_main.add(MenuButton(l_settings_screen, target=self.options_menu_screen, \
            widget_properties=self.widget_properties, pos_size=pos_size), 'center')
        self.options_menu_main.add(MenuButton(l_settings_sound, target=self.options_menu_sound, \
            widget_properties=self.widget_properties, pos_size=pos_size), 'center')
        self.options_menu_main.add(MenuButton(l_settings_theme, target=self.options_menu_theme, \
            widget_properties=self.widget_properties, pos_size=pos_size), 'center')
        self.options_menu_main.add(MenuButton(l_settings_misc, target=self.options_menu_misc, \
            widget_properties=self.widget_properties, pos_size=pos_size), 'center')

        back_from_screen = MenuButton(l_back, target=self.options_menu_main, \
            widget_properties=self.widget_properties)
        back_from_sound = MenuButton(l_back, target=self.options_menu_main, \
            widget_properties=self.widget_properties)
        back_from_theme = MenuButton(l_back, target=self.options_menu_main, \
            widget_properties=self.widget_properties)
        back_from_misc = MenuButton(l_back, target=self.options_menu_main, \
            widget_properties=self.widget_properties)
        save_button = MenuButton(l_save, function=self.save, \
            widget_properties=self.widget_properties)
        save_quit_button = MenuButton(l_save_quit, function=self.save, \
            args='quit', widget_properties=self.widget_properties)

        # Add items to settings menus:
        self.options_menu_screen.add(back_from_screen, 'center')
        self.options_menu_screen.add(save_button, 'center')
        self.options_menu_screen.add(save_quit_button, 'center')

        self.options_menu_sound.add(back_from_sound, 'center')
        self.options_menu_sound.add(save_button, 'center')
        self.options_menu_sound.add(save_quit_button, 'center')

        self.options_menu_theme.add(back_from_theme, 'center')
        self.options_menu_theme.add(save_button, 'center')
        self.options_menu_theme.add(save_quit_button, 'center')

        self.options_menu_misc.add(back_from_misc, 'center')
        self.options_menu_misc.add(save_button, 'center')
        self.options_menu_misc.add(save_quit_button, 'center')


        res = str(self.screen_res_x) + 'x' + str(self.screen_res_y)
        if res in self.disp.valid_resolutions:
            selected_resolution = \
                self.disp.valid_resolutions.index(res)
        else:
            selected_resolution = 2

        screen_items = []
        screen_items.append({'info' : i_resolution,
                    'button_type' : 'toggle',
                    'toggle_items' : self.disp.valid_resolutions,
                    'selected_item' : selected_resolution})
        screen_items.append({'info' : i_fullscreen, 'button_type' : 'toggle', \
                    'toggle_items' : on_off_toggle,
                    'selected_item' : self.fullscreen_on})
        screen_items.append({'info' : i_fps_label, 'button_type' : 'toggle', \
                    'toggle_items' : on_off_toggle,
                    'selected_item' : self.fps_label})
        screen_items.append({'info' : i_pil, 'button_type' : 'toggle', \
                    'toggle_items' : on_off_toggle, \
                    'selected_item' : self.use_pil})
        screen_group = {'heading' : h2_settings_screen, 'items' : screen_items}
        self.options_menu_screen.add_group(screen_group)


        misc_items = []
        misc_items.append({'info' : i_lan,
                    'button_type' : 'toggle',
                    'toggle_items' : valid_languages,
                    'selected_item' : self.locale})
        misc_items.append({'info' : i_octave,
                    'button_type' : 'toggle',
                    'toggle_items' : on_off_toggle,
                    'selected_item' : self.octave})

        misc_group = {'heading' : h2_settings_misc, 'items' : misc_items}
        self.options_menu_misc.add_group(misc_group)


        if self.sound_player in self.valid_sound_players:
            self.selected_player = self.valid_sound_players.index(self.sound_player)
        else:
            self.selected_player = 1 # defaults to PyGame
        sound_items = []
        sound_items.append({'info' : i_sound_output,
                    'button_type' : 'toggle',
                    'toggle_items' : self.valid_sound_players,
                    'selected_item' : self.selected_player})

        if self.sound_input in self.valid_sound_inputs:
            self.selected_input = self.valid_sound_inputs.index(self.sound_input)
        else:
            self.selected_input = 0 # defaults to OSS

        sound_items.append({'info' : i_sound_input,
                    'button_type' : 'toggle',
                    'toggle_items' : self.valid_sound_inputs,
                    'selected_item' : self.selected_input})

        sound_items.append({'info' : i_song_preview,
                    'button_type' : 'toggle',
                    'toggle_items' : on_off_toggle,
                    'selected_item' : self.sound_preview})

        sound_group = {'heading' : h2_settings_sound, 'items' : sound_items}
        self.options_menu_sound.add_group(sound_group)

        available_themes = self.theme_mgr.get_theme_names(os.path.join(self.app_dir, 'themes'))

        if self.theme_name in available_themes:
            selected_theme = available_themes.index(self.theme_name)
        else: selected_theme = 0
        theme_items = []
        theme_items.append({'info' : i_theme,
                    'button_type' : 'toggle',
                    'toggle_items' : available_themes,
                    'selected_item' : selected_theme})
        theme_group = {'heading': h2_settings_theme, 'items' : theme_items}
        self.options_menu_theme.add_group(theme_group)

        # Add buttons to main menu:
        sing_args = {}
        sing_args['selected'] = sing_screen
        sing_args['widgets'] = [main_menu]
        main_menu.add(MenuButton(l_start, target=song_browser, function=song_browser.start_song,\
            widget_properties=self.widget_properties, pos_size=pos_size), 'center')

        edit_args = {}
        edit_args['selected'] = song_editor
        edit_args['widgets'] = [main_menu]
        main_menu.add(MenuButton(l_song_editor, target=song_editor_browser, function=song_editor_browser.start_song,\
            widget_properties=self.widget_properties, pos_size=pos_size), 'center')

        main_menu.add(MenuButton(l_settings_main, target=self.options_menu_main, \
            widget_properties=self.widget_properties, pos_size=pos_size), 'center')
        main_menu.add(MenuButton(l_about, target=about_menu, \
            widget_properties=self.widget_properties, pos_size=pos_size), 'center')
        main_menu.add(MenuButton(l_quit2, function=self.quit, args=0, \
            widget_properties=self.widget_properties, pos_size=pos_size), 'center')

        # hide the loading label:
        self.loading_cont.visible = 0

        # logo:
        if self.use_pil and show_logo:
            try:
                logo = pudding.control.Logo(self.root_widget, logo_path, z_index=4)
            except:
                pass

        main_menu.show()
        pudding.main_loop.MainLoop(self.root_world).idle()


    def save(self, args=None):
        # Sucking values out of the pudding labels, wich is crap:
        x, y = self.options_menu_screen.toggle_list[0].label.split('x')
        fs = self.options_menu_screen.toggle_list[1].label
        fps = self.options_menu_screen.toggle_list[2].label
        pil = self.options_menu_screen.toggle_list[3].label

        sp = self.options_menu_sound.toggle_list[0].label
        si = self.options_menu_sound.toggle_list[1].label
        spr = self.options_menu_sound.toggle_list[2].label

        tn = self.options_menu_theme.toggle_list[0].label

        locale = self.options_menu_misc.toggle_list[0].label
        octave = self.options_menu_misc.toggle_list[1].label

        self.config['screen'] = {
            'resolution_x' : x,
            'resolution_y' : y,
            'fullscreen' : fs,
            'fps_label' : fps,
            'pil' : pil
        }
        self.config['sound'] = {
            'player' : sp,
            'input' : si,
            'preview' : spr,
        }
        self.config['theme'] = {
            'name' : tn
        }
        self.config['misc'] = {
            'locale' : locale,
            'octave' : octave
        }
        self.config.write()

        if args == 'quit':
            soya.quit()
            self._start()


    def quit(self, args=None):
        sys.exit(args)


def main():
    pass

if __name__ == '__main__': main()
