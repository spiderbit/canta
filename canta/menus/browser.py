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

import codecs
import sys
import os
import time
import soya.pudding as pudding
from canta.menus.menu import Menu
from canta.menus.button import MenuButton


from canta.theme.rotating_body import RotatingBody
from PIL import Image
import soya.pudding.ext.slicingimage

class MenuBrowser(Menu):
    def __init__(self, browsable_items, widget_properties, \
            use_pil=False, preview=False, octave=False, player=None, debug=False):
        Menu.__init__(self, widget_properties)

        l_next = _(u'next >>')
        l_prev = _(u'<< previous')
        self.l_artist = ""#'Artist: '
        self.l_title = ""#'Title: '
        self.l_description = ""#'Decription: '
        self.l_genre = str(_('Genre: '))
        self.l_edition = str(_('Edition: '))
        self.l_creator = str(_('Creator: '))
        self.l_bpm = str(_('BPM: '))
        self.l_start = str(_('Sing'))

        # heading and nav container inherited from Menu:
        self.widgets.append(self.heading_cont)
        self.widgets.append(self.nav_cont)

        self.browsable_items = browsable_items
        self.widget_properties = widget_properties
        self.use_pil = use_pil
        self.preview_sound = preview
        self.debug = debug

        self.item_containers = []
        self.selected_item = 0
        
        prev_button = MenuButton(label=l_prev, widget_properties=self.widget_properties, function=self.select_prev)
        next_button = MenuButton(l_next, function=self.select_next, widget_properties=self.widget_properties)
        self.add(prev_button, 'center')
        self.add(next_button, 'center')

        self.selected = 0
        self.cover_loaded = False
        pos_size = {}
        pos_size['top'] = 10
        pos_size['left'] = 10
        scr_top = self.box_cont.top + 20
        scr_right = 75
        scr_width = self.screen_res_x - 20
        scr_height = self.screen_res_y - 20
        self.player = player

        self.cover_cont = pudding.container.VerticalContainer( \
            self.parent_widget, top=scr_top + 120, \
            right=scr_right, width=scr_width, \
            height=scr_height)
        self.cover_cont.left = 40
        self.cover_cont.anchors = pudding.ANCHOR_ALL
        self.cover_cont.padding = 10
        self.cover_cont.visible = 0

        self.scroll_cont = pudding.container.VerticalContainer( \
            self.parent_widget, top=scr_top, \
            right=scr_right, width=scr_width, \
            height=scr_height)
        self.scroll_cont.left = 40
        self.scroll_cont.anchors = pudding.ANCHOR_ALL
        self.scroll_cont.padding = 10
        self.scroll_cont.visible = 0

        self.desc_cont = pudding.container.VerticalContainer( \
            self.parent_widget, top=scr_top + 120, \
            right=75, width=10, \
            height=10)
        self.desc_cont.left = self.screen_res_x / 3. + 50 #350
        self.desc_cont.anchors = pudding.ANCHOR_ALL
        self.desc_cont.padding = 10
        self.desc_cont.visible = 0

        pos_size['height'] = self.screen_res_y / 10
        pos_size['width'] = self.screen_res_x - 20
        self.start_button = MenuButton('No Songs found', widget_properties = self.widget_properties, pos_size=pos_size)
        self.scroll_cont.add_child(self.start_button, \
                pudding.EXPAND_HORIZ)

        self.desc_label = pudding.control.SimpleLabel( \
                label='', autosize=True, \
                font=self.font_p, top=0, \
                left=0, color=self.color_p)

        self.desc_cont.add_child(self.desc_label)

        self.item_containers.append(self.scroll_cont)
        self.widgets.append(self.scroll_cont)
        self.widgets.append(self.cover_cont)
        self.widgets.append(self.desc_cont)


            
    def stop_preview(self):
        if self.preview_sound:
            self.player.stop()

    def load_cover(self, song):
        wanted_size = self.screen_res_x / 3.
        if 'cover' in song.info:
            pic_path = os.path.join(song.path, song.info['cover'])
            pil_pic = Image.open(pic_path)
            bigger_size = max(pil_pic.size)
            factor = bigger_size / wanted_size
            size_x = pil_pic.size[0] / factor
            size_y = pil_pic.size[1] / factor
            size = (int(size_x), int(size_y))
        
            pil_pic = pil_pic.resize(size, Image.ANTIALIAS)
            if self.cover_loaded:
                del self.cover_cont.children[0:]

            self.cover_image = pudding.ext.slicingimage.SlicingImage( \
                parent=self.cover_cont, \
                pil_image=pil_pic, top=0,\
                left=0, z_index=-3)

            self.cover_loaded = True

        elif self.cover_loaded:
            del self.cover_cont.children[0:]

        self.parent_widget.on_resize()


    def start_song(self):
        self.select_song('start')

    def select_prev(self):
        self.select_song('prev')


    def select_next(self):
        self.select_song('next')


    def select_song(self, type):
        if len(self.browsable_items) == 0:
            return

        if type == 'prev':
            self.selected -= 1

        elif type == 'next':
            self.selected += 1
        elif type == 'start':
            self.selected = 0

        if self.debug:
            print self.selected

        self.selected %= len(self.browsable_items)
        song = self.browsable_items[self.selected]

        # Song preview:
        self.player.load(song.path, song.info['mp3'])
        if self.preview_sound:
            self.player.play()

        song_title = song.info['title']
        l = self.l_start + ':  "' + song_title + '"'
        self.start_button.args = [song, self.widgets]
        self.start_button.label = l
        self.desc_label.label = self.get_desc(song)
        self.desc_label.on_resize()

        # We use PIL only if it's set since it causes errors on some
        # systems (ATI drivers especially).
        if self.use_pil:
            self.load_cover(song)


    def select(self, function, args):
        function(args)


    def add(self, button, align='center'):
        """Add a button to the navi container as child"""
        self.nav_cont.add_child(button, pudding.EXPAND_BOTH)
        button.root=self


    def get_desc(self, song):
        """Return a string with the song info"""
        desc = ''

        # Dynamic solution (black):
        # It's just two lines, but I did not use it because it's
        # too much info, e.g. gap, start, ... (too technical).
        #for value in song.info:
        #	desc += value + '\n'

        # Static solution:
        if song.info['artist'] != "":
            desc += self.l_artist + song.info['artist'] + '\n'
        if 'title' in song.info:
            desc += self.l_title + song.info['title'] + '\n'
        if 'description' in song.info:
            desc += self.l_description + song.info['description'] + '\n'
        if 'genre' in song.info:
            desc += self.l_genre + song.info['genre'] + '\n'
        if 'edition' in song.info:
            desc += self.l_edition + song.info['edition'] + '\n'
        if 'creator' in song.info:
            desc += self.l_creator + song.info['creator'] + '\n'
#		if 'bpm' in song.info:
#			desc += self.l_bpm + str(round(song.info['bpm'], 1)) + '\n'
        return desc


