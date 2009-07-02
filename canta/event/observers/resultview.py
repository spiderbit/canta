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
import soya.pudding.ext.slicingimage
import soya.pudding.ext.meter
from PIL import Image

class ResultView(ContentMenu):
    def __init__(self, widget_properties, main_menu, browser, song=None, \
            use_pil=False, game=None):

        self.l_main_menu = _(u'main menu')
        self.l_choose = _(u'choose another song')
        self.l_quit = _(u'quit')
        #self.separator = ' - '
        self.l_points = {}
        self.l_points['normal'] = _(u'normal points')
        self.l_points['freestyle'] = _(u'freestyle points')
        self.l_points['bonus'] = _(u'bonus points')
        self.l_points['sum'] = _(u'points')
        self.l_score = _(u'SCORE')

        ContentMenu.__init__(self, widget_properties)
        # heading, nav and box container inherited from Menu:

        self.widget_properties = widget_properties
        self.main_menu = main_menu
        self.browser = browser
        self.song = song
        self.use_pil = use_pil
        self.theme_mgr = self.widget_properties['theme_mgr']

        self.world = soya.World()
        self.parent_world.add(self.world)

        self.main_theme_name = self.widget_properties['theme']['main']
        self.song_theme_name = self.widget_properties['theme']['song']

        self.values = []
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

        font_p = self.widget_properties['font']['p']['obj']
        color_p = self.widget_properties['font']['p']['color']
        self.res_label = pudding.control.SimpleLabel(
                    label=u'',
                    font=font_p,
                    color=color_p,
                    top=10,
                    left=10)

        # Add a button that leads to the main menu:
        self.add(MenuButton(label=self.l_main_menu, \
                target=self.main_menu,  \
                widget_properties=self.widget_properties), \
                'center')

        # Add a button that leads to the SongBrowser:
        self.add(MenuButton(label=self.l_choose, \
                target=self.browser, \
                widget_properties=self.widget_properties), \
                'center')

        # Add a quit button:
        self.add(MenuButton(label=self.l_quit, \
                function=self.quit, \
                widget_properties=self.widget_properties), \
                'center')

        point_order = ('normal', 'freestyle', 'bonus', 'sum')
        for p in point_order:
            self.res_label.label += '{0}: {1!s}/{2!s}\n'.format(
                self.l_points[p], self.game.get_points(p),
                self.game.get_points_possible(p))

        points = self.game.get_points()
        points_possible = self.game.get_points_possible()

        if points == 0:
            per_cent_right = float(0)
        else:
            per_cent_right =   (float(points) \
                / float(points_possible) ) * 100.

        swells = ( 97, 90, 80, 68, 53, 35, 0 )
        scores = ( 'A+', 'A', 'B', 'C', 'D', 'E', 'F' )
        # 7 Colors from hot to warm (100% to 0%):
        alpha = 0.8
        colors = []
        colors.append((0.9, 0.1, 0.0, alpha))
        colors.append((1.0, 0.6, 0.0, alpha))
        colors.append((0.9, 0.8, 0.0, alpha))
        colors.append((0.0, 0.8, 0.1, alpha))
        colors.append((0.0, 0.8, 0.8, alpha))
        colors.append((0.2, 0.3, 0.7, alpha))
        colors.append((0.2, 0.0, 0.4, alpha))
        for swell, _score, color in zip(swells, scores, colors):
            if per_cent_right >= swell:
                score = _score
                col = color
                break
        self.res_label.label += '\n{0}: {1!s}'.format(self.l_score, score)

        # Add the result meter (percentage):
        self.result_meter = pudding.ext.meter.Meter(min=0, max=100, \
            left=10, top=10, width=200, height=50)

        if points == 0:
            per_cent_right = float(0)
        else:
            per_cent_right =   (float(points) \
                / float(points_possible) ) * 100.

        self.result_meter.color = col
        self.result_meter.border_color = self.bg_box.border_color
        self.result_meter.background_color = self.bg_box.background_color
        self.result_meter.user_change = False
        self.result_meter.__set_value__(per_cent_right)

        self.main_theme_name = self.widget_properties['theme']['main']
        self.song_theme_name = self.widget_properties['theme']['song']
        if self.song_theme_name is not None:
            self.theme_mgr.hide_theme(self.song_theme_name)
            self.theme_mgr.show_theme(self.widget_properties['theme']['main'])
            self.widget_properties['theme']['song'] = None

        self.results_cont.add_child(self.result_meter, pudding.EXPAND_HORIZ)
        self.results_cont.add_child(self.res_label, pudding.EXPAND_HORIZ)
        self.add_child(self.results_cont)

        self.parent.on_resize()
        self.show()


    def update(self, subject):
        status = subject.data['type']
        if status == 'end':
            "end sendet"
            self._end()


    def add(self, button, align = 'left'):
        self.nav_cont.add_child(button, pudding.EXPAND_BOTH)
        button.root=self


    def quit(self, args=None):
        sys.exit(0)

