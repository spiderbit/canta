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


class MenuBrowserPresentation(Menu):
    def __init__(self, widget_properties):
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
        self.l_start = str(_('Enter'))
        self.widget_properties = widget_properties

        # heading and nav container inherited from Menu:
        self.widgets.append(self.heading_cont)
        self.widgets.append(self.nav_cont)
        self.prev_button = MenuButton(label=l_prev, widget_properties=self.widget_properties)
        self.next_button = MenuButton(l_next, widget_properties=self.widget_properties)
        self.add(self.prev_button, 'center')
        self.add(self.next_button, 'center')
        pos_size = {}
        pos_size['top'] = 10
        pos_size['left'] = 10
        scr_top = self.box_cont.top + 20
        scr_right = 75
        scr_width = self.screen_res_x - 20
        scr_height = self.screen_res_y - 20

        self.directory_cont = pudding.container.HorizontalContainer( \
            self.parent_widget, top=scr_top + 60, \
            right=scr_right, width=scr_width, \
            height=scr_height)
        self.directory_cont.left = 180

        self.cover_cont = pudding.container.VerticalContainer( \
            self.parent_widget, top=scr_top + 120, \
            right=scr_right, width=scr_width, \
            height=scr_height)
        self.cover_cont.left = 40

        self.scroll_cont = pudding.container.VerticalContainer( \
            self.parent_widget, top=scr_top, \
            right=scr_right, width=scr_width, \
            height=scr_height)
        self.scroll_cont.left = 40

        self.desc_cont = pudding.container.VerticalContainer( \
            self.parent_widget, top=scr_top + 120, \
            right=75, width=10, \
            height=10)
        self.desc_cont.left = self.screen_res_x / 3. + 50 #350

        container = [self.desc_cont, self.scroll_cont, \
            self.cover_cont, self.directory_cont]
        for c in container:
            c.anchors = pudding.ANCHOR_ALL
            c.padding = 10
            c.visible = 0

        pos_size['height'] = self.screen_res_y / 10
        pos_size['width'] = self.screen_res_x - 20
        self.start_button = MenuButton('No Songs found', \
            widget_properties = self.widget_properties, pos_size=pos_size)
        self.scroll_cont.add_child(self.start_button, \
                pudding.EXPAND_HORIZ)

        pos_size['height'] = self.screen_res_y / 10
        pos_size['width'] = self.directory_cont.left + 50

        pos_size['height'] = self.screen_res_y / 10
        pos_size['width'] = self.directory_cont.left + 10

        self.directory_up_button = MenuButton("<<", \
            widget_properties = self.widget_properties, pos_size=pos_size)
        self.directory_cont.add_child(self.directory_up_button, \
                pudding.ALIGN_LEFT)

        self.choose_base_button = MenuButton("", \
            widget_properties = self.widget_properties, pos_size=pos_size)
        self.directory_cont.add_child(self.choose_base_button, \
                pudding.ALIGN_LEFT)

        self.desc_label = pudding.control.SimpleLabel( \
                label='', autosize=True, \
                font=self.font_p, top=0, \
                left=0, color=self.color_p)

        self.desc_cont.add_child(self.desc_label)
        self.item_containers = []
        self.item_containers.append(self.scroll_cont)
        for c in container:
            self.widgets.append(c)


class MenuBrowser(MenuBrowserPresentation):
    def __init__(self, song_managers, default_manager, widget_properties, \
            use_pil=False, preview=False, octave=False, player=None, \
            entry_start_texts=None, start_screen=None):
        MenuBrowserPresentation.__init__(self, widget_properties)
        self.cover_loaded = False
        self.player = player
        self.song_managers = song_managers
        self.default_manager = self.selected_manager = default_manager
        self.use_pil = use_pil
        self.preview_sound = preview
        self.start_screen = start_screen
        self.current_entry = 0
        self.entry_start_texts = entry_start_texts
        self.browsable_items = self.song_managers[default_manager].get_entries()
        self.dir_pos = ''
        self.choose_base_button.label = self.song_managers[default_manager].name
        self.select_song('start')
        self.directory_up_button.function = self.directory_up
        self.choose_base_button.function = self.choose_base
        self.prev_button.function=self.select_prev
        self.next_button.function=self.select_next
        if len(self.browsable_items) > 0:
            self.start_button.args = [self.browsable_items[ \
                self.browsable_items.keys()[self.current_entry]], self.widgets]
            self.start_button.function = self.clean_start


    def choose_base(self):
        self.selected_manager += 1
        self.selected_manager %= len(self.song_managers)
        self.browsable_items = self.song_managers[self.selected_manager].get_entries()
        self.select_song('start')
        self.choose_base_button.label = self.song_managers[self.selected_manager].name
        self.choose_base_button.on_resize()

    def directory_up(self):
        entry_pos_str = self.dir_pos.split('/')[-1]
        self.dir_pos = "/".join(self.dir_pos.split('/')[:-1])
        self.browsable_items = self.song_managers[self.selected_manager].get_entries(self.dir_pos)
        entry_pos = self.browsable_items.keys().index(entry_pos_str)
        self.select_song('set_pos', entry_pos)

    def enter_sub_directory(self, args):
        self.dir_pos = os.path.join(self.dir_pos, args[0])
        self.enter_directory(0)

    def enter_directory(self, pos):
        self.browsable_items = self.song_managers[self.selected_manager].get_entries(self.dir_pos)
        self.select_song('set_pos', pos)

    def stop_preview(self):
        if self.preview_sound:
            self.player.stop()

    def get_cover(self, song):
        cover = None
        if 'cover' in song.info:
            cover = os.path.join(song.path, song.info['cover'])
        return cover

    def load_cover(self, pic_path):
        wanted_size = self.screen_res_x / 3.
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
        self.parent_widget.on_resize()


    def start_song(self):
        self.select_song('start')

    def select_prev(self):
        self.select_song('prev')

    def select_next(self):
        self.select_song('next')


    def select_song(self, direction, pos=None):
        if len(self.browsable_items) == 0:
            return

        self.selected = self.browsable_items.keys()
        if direction == 'prev':
            self.current_entry -= 1
        elif direction == 'next':
            self.current_entry += 1
        elif direction == 'start':
            self.current_entry = 0
        elif direction == 'set_pos':
            self.current_entry = pos

        self.current_entry %= len(self.browsable_items)
        l = ""

        entry = self.browsable_items[self.browsable_items.keys()[self.current_entry]]
        if type(entry) != list:
            self.l_start = self.entry_start_texts['song']
            # Song preview:
            song = entry
            self.start_button.function = self.start_screen.show
            self.player.load(song.path, song.info['mp3'])
            if self.preview_sound:
                self.player.play()

            song_title = song.info['title']
            l = self.l_start + ':  "' + song_title + '"'
            self.start_button.args = [song, self.widgets]
            self.desc_label.label = self.get_desc(song)

            # We use PIL only if it's set since it causes errors on some
            # systems (ATI drivers especially).
            if self.use_pil:
                pic_path = self.get_cover(song)
                if pic_path:
                    self.load_cover(pic_path)
        else:
            self.l_start = self.entry_start_texts['directory']
            self.start_button.function = self.enter_sub_directory

            dir_name = self.browsable_items.keys()[self.current_entry]
            self.start_button.args = [dir_name]

            l = self.l_start + ':  "' + "Directory >> " + dir_name + '"'
            self.desc_label.label = ''

            app_dir = os.path.dirname(sys.argv[0])
            # We use PIL only if it's set since it causes errors on some
            # systems (ATI drivers especially).
            if self.use_pil:
                pic_path = os.path.join(app_dir, 'misc', 'directory.png')
                self.load_cover(pic_path)
        self.start_button.label = l
        self.desc_label.on_resize()


    def select(self, function, args):
        function(args)


    def add(self, button, align='center'):
        """Add a button to the navi container as child"""
        self.nav_cont.add_child(button, pudding.EXPAND_BOTH)
        button.root=self

    def clean_start(self, args):
        self.stop_preview()
        if len(self.browsable_items) > 0:
            self.start_screen.show(args)

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

