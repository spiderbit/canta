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
import user
import soya.pudding as pudding
from canta.menus.menu import Menu
from canta.menus.button import MenuButton
from canta.song.song_manager import *

from canta.theme.rotating_body import RotatingBody
from PIL import Image
import soya.pudding.ext.slicingimage


class MenuBrowserPresentation(Menu):
    def __init__(self, widget_properties):
        Menu.__init__(self, widget_properties)
        l_next = _(u'next >>')
        l_prev = _(u'<< previous')

        self.prev_button = MenuButton(label=l_prev, \
            widget_properties=self.widget_properties)
        self.next_button = MenuButton(l_next, \
            widget_properties=self.widget_properties)
        self.add(self.prev_button, 'center')
        self.add(self.next_button, 'center')

        self.bc_top = self.nc_top + 10 + self.nc_height
        self.bc_left = 20
        self.bc_width = self.screen_res_x - 40
        self.bc_height = self.screen_res_y - self.bc_top - 25
        self.bc_right = 20
        self.bc_bottom = 30
        self.box_cont = pudding.container.Container( \
                self, left=self.bc_left, top=self.bc_top, \
                width=self.bc_width, height=self.bc_height, \
                right=self.bc_right)

        self.bg_box = pudding.control.Box(self.box_cont, \
                width=self.bc_width, \
                height=self.bc_height, \
                background_color=self.box_bg_color, \
                border_color=self.box_border_color, \
                z_index=-3)
        self.bg_box.anchors = pudding.ANCHOR_ALL

        self.directory_cont = pudding.container.HorizontalContainer( \
            self.box_cont, top=self.height * 0.02, \
            right=self.right, width=self.width, \
            height=self.height, left=0)

        pos_size = {}
        pos_size['top'] = 0
        pos_size['left'] = 0
        pos_size['height'] = self.height * 0.05
        pos_size['width'] = self.width * 0.3

        self.directory_cont.anchors = pudding.ANCHOR_ALL
        self.directory_cont.padding = 10

        self.directory_up_button = MenuButton("<<", \
            widget_properties = self.widget_properties, pos_size=pos_size)
        self.directory_cont.add_child(self.directory_up_button, \
                pudding.ALIGN_LEFT)

        pos_size = {}
        pos_size['top'] = 0
        pos_size['left'] = self.width * 0.9
        pos_size['height'] = self.height * 0.05
        pos_size['width'] = self.width * 0.3

        self.choose_base_button = MenuButton("", \
            widget_properties = self.widget_properties, pos_size=pos_size)
        self.directory_cont.add_child(self.choose_base_button, \
                pudding.ALIGN_RIGHT)



class MenuBrowser(MenuBrowserPresentation):
    def __init__(self, default_manager, widget_properties, sing_screen,\
             config=None, player=None, song_start_text='enter'):
        MenuBrowserPresentation.__init__(self, widget_properties)
        self.config = config
        self.cover_loaded = False
        self.player = player
        self.song_managers = []
        self.default_manager = self.selected_manager = default_manager
        self.use_pil = self.config['screen'].as_bool('pil')
        self.preview = self.config['sound'].as_bool('preview')
        self.prev_button.function=self.select_prev
        self.next_button.function=self.select_next
        app_dir = os.path.dirname(sys.argv[0])
        self.config_path = os.path.join(user.home, '.canta')
        self.song_start_text = song_start_text
        directories = []
        sys_directory = {}
        sys_directory['name'] = 'System'
        sys_directory['path'] = Directory(os.path.join(app_dir, 'media', 'songs'))
        home_directory = {}
        home_directory['name'] = 'Home'
        home_directory['path'] = Directory(os.path.join(self.config_path, 'songs'))
        directories.append(sys_directory)
        directories.append(home_directory)
        for directory in directories:
            song_manager = SongManager( self, \
                directory['path'], sing_screen, player, directory['name'])
            song_manager.search()
            song_manager.verify()
            song_manager.sort()
            self.song_managers.append(song_manager)

        self.directory_up_button.function = self.directory_up
        self.choose_base_button.function = self.choose_base
        self.choose_base_button.label = song_manager.name


    def directory_up(self):
        self.song_managers[self.selected_manager].directory_up()

    def choose_base(self):
        self.selected_manager += 1
        self.selected_manager %= len(self.song_managers)
        self.browsable_items = self.song_managers[self.selected_manager].get_entries()
        self.reload_view('start')

    def stop_preview(self):
        if 'selected_entry' in self.__dict__:
            self.selected_entry.stop_preview()

    def start_song(self):
        self.reload_view('start')

    def select_prev(self):
        self.reload_view('prev')

    def select_next(self):
        self.reload_view('next')

    def reload_view(self, direction, pos=None):
        song_manager = self.song_managers[self.selected_manager]
        if song_manager.dir_pos!='':
            self.directory_up_button.visible=1
        else:
            self.directory_up_button.visible=0
        if len(song_manager.browsable_items) == 0:
            return
        song_manager.select_entry(direction, pos)
        entry = song_manager.browsable_items \
            [song_manager.browsable_items.keys()[song_manager.current_entry]]
        if 'selected_entry' in self.__dict__:
            self.selected_entry.hide()
            self.selected_entry.stop_preview()
        self.choose_base_button.label = song_manager.name
        self.selected_entry = entry
        self.selected_entry.left = self.bc_left
        self.selected_entry.top = self.bc_top
        self.selected_entry.width = self.bc_width
        self.selected_entry.height = self.bc_height
        self.selected_entry.right = self.bc_right
        self.selected_entry.show()



    def add(self, button, align='center'):
        """Add a button to the navi container as child"""
        # Deprecated
        self.nav_cont.add_child(button, pudding.EXPAND_BOTH)
        button.root=self

