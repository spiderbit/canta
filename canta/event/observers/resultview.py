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

import os
import sys
import soya
import soya.pudding as pudding
from canta.menus.menu import ContentMenu
from canta.menus.button import MenuButton
#import PIL.Image as pil
import soya.pudding.ext.slicingimage
import soya.pudding.ext.meter
from PIL import Image

class ResultView(ContentMenu):
    def __init__(self, widget_properties, menu_list, song=None, \
            use_pil=False, game=None, debug=False):

        self.l_main_menu = _(u'main menu')
        self.l_choose = _(u'choose another song')
        self.l_quit = _(u'quit')
        #self.separator = ' - '
        self.l_right_values = _(u'Right: ')
        self.l_wrong_values = _(u'Wrong: ')
        self.l_percental = _(u'Score: ')
        self.l_percent_symbol = u'%'

        ContentMenu.__init__(self, widget_properties)
        # heading, nav and box container inherited from Menu:

        self.widget_properties = widget_properties
        self.menu_list = menu_list
        self.song = song
        self.use_pil = use_pil
        self.theme_mgr = self.widget_properties['theme_mgr']
        self.debug = debug

        self.world = soya.World()
        self.parent_world.add(self.world)

        self.main_theme_name = self.widget_properties['theme']['main']
        self.song_theme_name = self.widget_properties['theme']['song']

        self.results = []
        self.pos = None
        self.game = game

    def _end(self):
        # If the played song had its own theme, we overwrite
        # the values with the menu theme:
        if self.song_theme_name is not None:
            # FIXME: Copied this stuff for now (blacki said I can do this
            # in a loop, but I must ask him again, how ):
            self.widget_properties['font']['lyrics']['to_sing'] = {}
            font_lyrics_ts = self.theme_mgr.get_font(self.main_theme_name, 'lyrics', 'to_sing', 'font')
            color_lyrics_ts = self.theme_mgr.get_font(self.main_theme_name, 'lyrics', 'to_sing', 'color')
            self.widget_properties['font']['lyrics']['to_sing']['obj'] = font_lyrics_ts
            self.widget_properties['font']['lyrics']['to_sing']['color'] = color_lyrics_ts

            self.widget_properties['font']['lyrics']['special'] = {}
            font_lyrics_spec = self.theme_mgr.get_font(self.main_theme_name, 'lyrics', 'special', 'font')
            color_lyrics_spec = self.theme_mgr.get_font(self.main_theme_name, 'lyrics', 'special', 'color')
            self.widget_properties['font']['lyrics']['special']['obj'] = font_lyrics_spec
            self.widget_properties['font']['lyrics']['special']['color'] = color_lyrics_spec

            self.widget_properties['font']['lyrics']['active'] = {}
            font_lyrics_act = self.theme_mgr.get_font(self.main_theme_name, 'lyrics', 'active', 'font')
            color_lyrics_act = self.theme_mgr.get_font(self.main_theme_name, 'lyrics', 'active', 'color')
            self.widget_properties['font']['lyrics']['active']['obj'] = font_lyrics_act
            self.widget_properties['font']['lyrics']['active']['color'] = color_lyrics_act

            self.widget_properties['font']['lyrics']['done'] = {}
            font_lyrics_done = self.theme_mgr.get_font(self.main_theme_name, 'lyrics', 'done', 'font')
            color_lyrics_done = self.theme_mgr.get_font(self.main_theme_name, 'lyrics', 'done', 'color')
            self.widget_properties['font']['lyrics']['done']['obj'] = font_lyrics_done
            self.widget_properties['font']['lyrics']['done']['color'] = color_lyrics_done

            self.widget_properties['font']['button']['on_focus'] = {}
            font_button_on = self.theme_mgr.get_font(self.main_theme_name, 'button', 'on_focus', 'font')
            color_button_on = self.theme_mgr.get_font(self.main_theme_name, 'button', 'on_focus', 'color')
            self.widget_properties['font']['button']['on_focus']['obj'] = font_button_on
            self.widget_properties['font']['button']['on_focus']['color'] = color_button_on

            self.widget_properties['font']['button']['off_focus'] = {}
            font_button_off = self.theme_mgr.get_font(self.main_theme_name, 'button', 'off_focus', 'font')
            color_button_off = self.theme_mgr.get_font(self.main_theme_name, 'button', 'off_focus', 'color')
            self.widget_properties['font']['button']['off_focus']['obj'] = font_button_off
            self.widget_properties['font']['button']['off_focus']['color'] = color_button_off

            self.widget_properties['box'] = self.theme_mgr.get_box(self.main_theme_name)
            self.bg_box.border_color = self.widget_properties['box']['border']['color']
            self.bg_box.background_color = self.widget_properties['box']['background']['color']

            self.widget_properties['button'] = self.theme_mgr.get_button(self.main_theme_name)

        # Add a container for meter and labels:
        res_top = self.screen_res_y / 10 + 40
        res_right = 75
        res_width = self.screen_res_x - 20
        res_height = self.screen_res_y - 20
        self.results_cont = pudding.container.VerticalContainer( \
                self, top=res_top, \
                right=res_right, width=res_width, \
                height=res_height)
        self.results_cont.left = 40
        self.results_cont.anchors = pudding.ANCHOR_ALL
        self.results_cont.padding = 20

        # Add a heading to the results (song name and artist):
        heading = ''
        if self.song.info['artist'] != '':
            heading += self.song.info['artist'] + '\n'
        if self.song.info['title'] != '':
            heading += self.song.info['title'] + '\n'

        if heading != '':
            font_h1 = self.widget_properties['font']['h1']['obj']
            color_h1 = self.widget_properties['font']['h1']['color']
            heading_label = pudding.control.SimpleLabel(
                    label=heading,
                    font=font_h1,
                    color=color_h1,
                    top=10,
                    left=10)
            self.results_cont.add_child(heading_label, pudding.EXPAND_HORIZ)

        # Add a cover image to the results:
        if self.use_pil:
            if 'cover' in self.song.info:
                wanted_size = self.screen_res_x / 4. #350.
                pic_path = os.path.join(self.song.path, self.song.info['cover'])
                pil_pic = Image.open(pic_path)
                bigger_size = max(pil_pic.size)
                factor = bigger_size / wanted_size
                size_x = pil_pic.size[0] / factor
                size_y = pil_pic.size[1] / factor
                size = (int(size_x), int(size_y))

                pil_pic = pil_pic.resize(size, Image.ANTIALIAS)
                self.cover_image = pudding.ext.slicingimage.SlicingImage( \
                    parent=self.results_cont, \
                    pil_image=pil_pic, top=0,\
                    left=0, z_index=-3)

        # Add the result meter (percentage):
        self.result_meter = pudding.ext.meter.Meter(min=0, max=100, \
            left=10, top=10, width=200, height=50)

        font_p = self.widget_properties['font']['p']['obj']
        color_p = self.widget_properties['font']['p']['color']
        self.res_label = pudding.control.SimpleLabel(
                    label=u'',
                    font=font_p,
                    color=color_p,
                    top=10,
                    left=10)

        self.results_cont.add_child(self.result_meter, pudding.EXPAND_HORIZ)
        self.results_cont.add_child(self.res_label, pudding.EXPAND_HORIZ)
        self.add_child(self.results_cont)

        # Add a button that leads to the main menu:
        main_menu = self.menu_list['main']
        self.add(MenuButton(label=self.l_main_menu, \
                target=main_menu,  \
                widget_properties=self.widget_properties), \
                'center')

        # Add a button that leads to the SongBrowser:
        show_browser = self.menu_list['browser']
        self.add(MenuButton(label=self.l_choose, \
                target=show_browser, \
                widget_properties=self.widget_properties), \
                'center')

        # Add a quit button:
        self.add(MenuButton(label=self.l_quit, \
                function=self.quit, \
                widget_properties=self.widget_properties), \
                'center')

        # Calculate results:
        right_values = 0
        wrong_values = 0

        for data in self.results:
            pitch = data['pitch']
            target_pitch = data['song'].get_pitch_between( \
                data['start_time'], data['end_time'])
            if pitch and target_pitch:
                pitch = self.game.get_corrected_pitch(target_pitch, pitch)
                difference = target_pitch - pitch
                if self.game.helper and difference <= self.game.allowed_difference:
                    right_values += 1
                else:
                    wrong_values += 1
            else:
                wrong_values += 1

        if len(self.results) == 0:
            per_cent_right = float(0)
        else:
            per_cent_right =   (float(right_values) \
                / len(self.results)) * 100.

        rv = self.l_right_values + str(right_values)
        wv = self.l_wrong_values + str(wrong_values)
        pc = self.l_percental + str(round(per_cent_right, 1)) + self.l_percent_symbol
        self.res_label.label =  pc + '\n' + rv + '\n' + wv

        # 7 Colors from warm to hot (0 to 100%):
        alpha = 0.8
        if per_cent_right < 15.:
            col = (0.2, 0.0, 0.4, alpha)
        elif per_cent_right < 30.:
            col = (0.2, 0.3, 0.7, alpha)
        elif per_cent_right < 45.:
            col = (0.0, 0.8, 0.8, alpha)
        elif per_cent_right < 60.:
            col = (0.0, 0.8, 0.1, alpha)
        elif per_cent_right < 75.:
            col = (0.9, 0.8, 0.0, alpha)
        elif per_cent_right < 90.:
            col = (1.0, 0.6, 0.0, alpha)
        else:
            col = (0.9, 0.1, 0.0, alpha)

        self.result_meter.color = col
        self.result_meter.border_color = self.bg_box.border_color
        self.result_meter.background_color = self.bg_box.background_color
        self.result_meter.user_change = False
        self.result_meter.__set_value__(per_cent_right)

        self.nav_cont.visible = 1
        self.box_cont.visible = 1
        self.results_cont.visible = 1

        self.main_theme_name = self.widget_properties['theme']['main']
        self.song_theme_name = self.widget_properties['theme']['song']
        if self.song_theme_name is not None:
            self.theme_mgr.hide_theme(self.song_theme_name)
            self.theme_mgr.show_theme(self.widget_properties['theme']['main'])
            self.widget_properties['theme']['song'] = None

        self.parent.on_resize()
        self.show()


    def update(self, subject):
        status = subject.data['type']
        if status == 'end':
            "end sendet"
            self._end()
        elif status == 'input':
            if 'pitch' in subject.data:
                self.set_value(subject.data)
        #elif status == 'activateNote':
        #    self.results.append({})

    def add(self, button, align = 'left'):
        self.nav_cont.add_child(button, pudding.EXPAND_BOTH)
        button.root=self


    def set_value(self, data):
        target_pitch = data['song'].get_pitch_between( \
            data['start_time'], data['end_time'])
        if not target_pitch:
            return
        self.results.append(data)


    def quit(self, args=None):
        sys.exit(0)

