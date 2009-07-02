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

import os
import sys
import time

import soya
import soya.pudding as pudding

from canta.event.song_event import SongEvent
from canta.event.keyboard_event import KeyboardEvent
from canta.event.subjects.song_data import SongData
from canta.event.observers.lyrics_observer import LyricsObserver
from canta.event.observers.main_cube_observer import MainCubeObserver
from canta.event.observers.sing_cube_observer import SingCubeObserver
from canta.event.observers.debug_widget import DebugWidget
from canta.event.observers.resultview import ResultView
from canta.event.observers.pos_cube_observer import PosCubeObserver
from canta.event.observers.music_notes import MusicNotes
from canta.event.observers.time_label import TimeLabel
from canta.event.observers.pause import Pause

from canta.game import Game

from canta.song.song import Song

from canta.menus.menu import Menu
from canta.menus.button import MenuButton

###   TEST   ### PygamePlayer
from canta.cameras.movable_camera import MovableCamera
### END TEST ###

class SingScreen(Menu):
    """Sing screen.
    """
    def __init__(self, app_dir, main_menu, camera, theme_mgr, widget_properties, \
            config, player=None):
        Menu.__init__(self, widget_properties)
        self.main_menu = main_menu
        self.app_dir = app_dir
        self.camera = camera
        self.theme_mgr = theme_mgr
        self.player = player
#        self.menu_list = {}
#        self.menu_list['singscreen'] = self
        self.config = config
        self.widget_properties['theme_mgr'] = theme_mgr


    def show(self, args):
        h1_pause = _(u'Pause')
        h1_results = _(u'Results')

        #self.camera = MovableCamera(self.app_dir, self.parent_world, debug = self.debug)
        self.camera.z = 15
        #self.parent.add_child(self.camera)

        self.song = args[0]
        self.song.reset()
        self.song.read()
        song_path = self.song.path
        self.song.split_in_lines()

        theme_cfg_file = os.path.join(song_path, 'theme_cfg.xml')

        if os.path.exists(theme_cfg_file):
            media_path = os.path.join(song_path, 'media')
            soya.path.append(media_path)

            self.theme_mgr.hide_theme(self.widget_properties['theme']['main'])
            theme_name = self.song.info['title']
            self.widget_properties['theme']['song'] = theme_name
            self.theme_mgr.get_theme(theme_name, song_path)
            self.theme_mgr.show_theme(theme_name)

            self.widget_properties['font']['lyrics']['to_sing'] = {}
            font_lyrics_ts = self.theme_mgr.get_font(theme_name, 'lyrics', 'to_sing', 'font')
            color_lyrics_ts = self.theme_mgr.get_font(theme_name, 'lyrics', 'to_sing', 'color')
            self.widget_properties['font']['lyrics']['to_sing']['obj'] = font_lyrics_ts
            self.widget_properties['font']['lyrics']['to_sing']['color'] = color_lyrics_ts

            self.widget_properties['font']['lyrics']['special'] = {}
            font_lyrics_spec = self.theme_mgr.get_font(theme_name, 'lyrics', 'special', 'font')
            color_lyrics_spec = self.theme_mgr.get_font(theme_name, 'lyrics', 'special', 'color')
            self.widget_properties['font']['lyrics']['special']['obj'] = font_lyrics_spec
            self.widget_properties['font']['lyrics']['special']['color'] = color_lyrics_spec

            self.widget_properties['font']['lyrics']['active'] = {}
            font_lyrics_act = self.theme_mgr.get_font(theme_name, 'lyrics', 'active', 'font')
            color_lyrics_act = self.theme_mgr.get_font(theme_name, 'lyrics', 'active', 'color')
            self.widget_properties['font']['lyrics']['active']['obj'] = font_lyrics_act
            self.widget_properties['font']['lyrics']['active']['color'] = color_lyrics_act

            self.widget_properties['font']['lyrics']['done'] = {}
            font_lyrics_done = self.theme_mgr.get_font(theme_name, 'lyrics', 'done', 'font')
            color_lyrics_done = self.theme_mgr.get_font(theme_name, 'lyrics', 'done', 'color')
            self.widget_properties['font']['lyrics']['done']['obj'] = font_lyrics_done
            self.widget_properties['font']['lyrics']['done']['color'] = color_lyrics_done

            self.widget_properties['font']['button']['on_focus'] = {}
            font_button_on = self.theme_mgr.get_font(theme_name, 'button', 'on_focus', 'font')
            color_button_on = self.theme_mgr.get_font(theme_name, 'button', 'on_focus', 'color')
            self.widget_properties['font']['button']['on_focus']['obj'] = font_button_on
            self.widget_properties['font']['button']['on_focus']['color'] = color_button_on

            self.widget_properties['font']['button']['off_focus'] = {}
            font_button_off = self.theme_mgr.get_font(theme_name, 'button', 'off_focus', 'font')
            color_button_off = self.theme_mgr.get_font(theme_name, 'button', 'off_focus', 'color')
            self.widget_properties['font']['button']['off_focus']['obj'] = font_button_off
            self.widget_properties['font']['button']['off_focus']['color'] = color_button_off

            self.widget_properties['box'] = self.theme_mgr.get_box(theme_name)
            self.widget_properties['button'] = self.theme_mgr.get_button(theme_name)

            self.widget_properties['bar'] = self.theme_mgr.get_bar(theme_name)

        img_observer = False
        song_theme_path = os.path.join(song_path, 'theme_cfg.xml')
        media_path = os.path.join(song_path, 'media')


        # The observer for the musical notes:
        music_notes = MusicNotes(self.parent_world)

        # Sizes and positions for the labels:
        pos_size = {}
        pos_size['width'] = 70
        pos_size['height'] = 30
        pos_size['left'] = 35
        self.widget_properties['pos_size'] = pos_size
        self.widget_properties['anchoring'] = 'bottom'

        # The observers for the lyrics:
        self.widget_properties['pos_size']['top'] = soya.get_screen_height() * 0.8
        lyrics_current = LyricsObserver(self.widget_properties)

        self.widget_properties['pos_size']['top'] = soya.get_screen_height() * 0.9
        lyrics_next = LyricsObserver(self.widget_properties, line_diff=1)

        use_pil = self.config['screen']['pil']
        self.game = Game(self.config)
        # The observer for the results screen (when the song ended):
        browser = args[1]
        result_view = ResultView(self.widget_properties, self.main_menu, \
                browser, self.song, use_pil, self.game)
        result_view.set_heading(h1_results)

        sing_bar_color = self.widget_properties['bar']['singbar']['color']
        sing_bar_formula = self.widget_properties['bar']['singbar']['formula']

        song_bar_color = {}
        song_bar_color['special'] = self.widget_properties['bar']['songbar']['special']['color']
        song_bar_color['freestyle'] = self.widget_properties['bar']['songbar']['freestyle']['color']
        song_bar_color['normal'] = self.widget_properties['bar']['songbar']['normal']['color']

        pos_bar_color = self.widget_properties['bar']['posbar']['color']

        # The observer for the symbolical musical representations:
        bar = MainCubeObserver(self.parent_world,
                       song_bar_color,
                       self.song.getMinPitch(),
                       self.song.getMaxPitch())

        # The observer for the microphone captured notes:
        input_bar = SingCubeObserver(self.parent_world,
                         sing_bar_color, sing_bar_formula,
                         self.song.getMinPitch(),
                         self.song.getMaxPitch(),
                         self.game)

        # The observer for the song position cube:
        pos_bar = PosCubeObserver(self.parent_world,
                      pos_bar_color)

        # Observer for the song time:
        time_label = TimeLabel(self.widget_properties)

        self.input_subject = SongData()
        self.input_subject.attach(input_bar)
        self.input_subject.attach(result_view)
        self.song_data = SongData()

        # maybe a subject-observer solution would be better
        # if we make would use it over network but for first release i think its good enough
        self.keyboard_event = KeyboardEvent(self.widget_properties)

        self.keyboard_event.add_connection(type = soya.sdlconst.K_ESCAPE, \
            action = self.pause)
        self.keyboard_event.add_connection(type = soya.sdlconst.K_q, \
            action = self.exit)
        self.keyboard_event.add_connection(type = soya.sdlconst.K_w, \
            action = soya.toggle_wireframe)
        self.keyboard_event.add_connection(type = soya.sdlconst.K_s, \
            action = self.make_screenshot)

        selected_input = self.config['sound']['input']
        if selected_input == 'Gstreamer':
            from canta.event.input_gstreamer import Input

        self.input = Input(self.song, self.input_subject, \
                self.player, self.config)

        self.song_event = SongEvent(self.song, self.widget_properties,\
                self.song_data, self.player, \
                self.keyboard_event, self.input)


        # Observer for the pause menu:
        pause = Pause(self.widget_properties, \
            self.song_data, self.player, self.keyboard_event, self.song, \
            self.song_event)
        pause.set_heading(h1_pause)

        self.song_data.attach(lyrics_current)
        self.song_data.attach(lyrics_next)
        self.song_data.attach(pos_bar)
        self.song_data.attach(bar)
        self.song_data.attach(time_label)
        self.song_data.attach(pause)
        self.song_data.attach(result_view)
        self.song_data.attach(input_bar)
        self.song_data.attach(music_notes)

        self.parent_world.add(self.keyboard_event)

        self.input.start()

        self.parent_world.add(self.song_event)
        self.player.load(self.song.path, self.song.info['mp3'])
        self.player.play()


    def pause(self):
        msg = {}
        if not self.player.paused:
            msg['type'] = 'paused'
            self.song_data.set_data(msg)
            self.parent_world.remove(self.keyboard_event)
            self.player.pause()

        else:
            msg['type'] = 'unpaused'
            self.song_data.set_data(msg)
            self.player.play()


    def exit(self):
        soya.MAIN_LOOP.stop()
        self.input.stop()
        self.input.join(0.1)
        sys.exit()


    def make_screenshot(self):
        filename = 'canta_' + str(time.strftime('%S' +'%H'+'%M'+'_'+'%d'+'-'+'%h'+'-'+'%Y'))+'.jpeg'
        soya.screenshot().save(os.path.join(os.path.dirname(sys.argv[0]), filename))

if __name__ == '__main__':
    pass

