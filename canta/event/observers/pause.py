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


import soya
import soya.pudding as pudding
from canta.menus.menu import Menu
from canta.menus.button import MenuButton

class Pause(Menu):
    def __init__(self, widget_props, song_data=None, \
            player=None, keyboard_event=None, song=None, \
            song_event=None):
        Menu.__init__(self, widget_props)
        l_continue = _(u'continue singing')
        l_quit = _(u'quit song')

        self.song_data = song_data
        self.song = song
        self.player = player
        self.keyboard_event = keyboard_event
        self.song_event = song_event

        args = {}
        args['widgets'] = [self]
        self.add(MenuButton(label=l_quit, \
                function=self._end, args=args, \
                widget_properties=widget_props), 'horiz')
        self.add(MenuButton(label=l_continue, \
                function=self.continue_song, args=args, \
                widget_properties=widget_props), 'horiz')


    def continue_song(self, args):		# i(stefan) think that we dont use that method anymore
        self.hide()
        self.parent_world.add(self.keyboard_event)
        self.player.play()


    def _end(self, args):
        self.visible = 0
        msg = {}
        msg['type'] = 'end'
        self.song_data.set_data(msg)
        self.song.end = True
        self.song_event.end_sended = True

    def _pause_song(self):
        self.on_resize()
        self.show()

    def update(self, subject):
        status = subject.data['type']
        if status == 'paused':
            self._pause_song()
        #elif status == 'unpaused':
        #	continue_song()
        #if status == 'end':
            #self._end()

