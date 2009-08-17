#! /usr/bin/python -O
# -*- coding: utf-8 -*-
#
#    CANTA - A free entertaining educational software for singing
#    Copyright (C) 2007  S. Huchler, A. Kattner, F. Lopez
#    Copyright (C) 2009  S. Huchler
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

"""Module browser_entry

Entries for the Menubrowser
"""

import os
import sys
from canta.menus.menu import Menu
from canta.menus.button import MenuButton
import soya.pudding as pudding

class CommonEntryPresentation(pudding.container.Container):
    def __init__(self, parent=None, width=0, \
        height=0, top=0, left=0, right=0, \
        bottom=0, anchors=0, padding=0):
        pudding.container.Container.__init__(self, parent=parent,\
            width=width, height=height, top=top, left=left, right=right, \
                bottom=bottom, anchors=anchors, padding=padding)
        self.font_p = self.parent.font_p
        self.color_p = self.parent.color_p
        self.widget_properties = self.parent.widget_properties
        self.visible=0

        pos_size = {}
        pos_size['top'] = self.height *0.1
        pos_size['left'] = self.width*0.25
        pos_size['width'] = self.width/2
        pos_size['height'] = self.height / 10

        self.start_button = MenuButton('No Songs found',\
            widget_properties = self.widget_properties, pos_size=pos_size)
        self.add_child(self.start_button, \
                pudding.EXPAND_HORIZ)


class SongEntryPresentation(CommonEntryPresentation):
    def __init__(self, parent=None, width=0, \
        height=0, top=0, left=0, right=0, \
        bottom=0, anchors=0, padding=0):
        CommonEntryPresentation.__init__(self, parent=parent, \
            width=width, height=height, top=top, left=left, \
                right=right, bottom=bottom, anchors=anchors, \
                    padding=padding)

        scr_top = self.height * 1 / 3
        scr_right = self.right
        scr_width = self.parent.screen_res_x
        scr_height = self.parent.screen_res_y
        self.cover_cont = pudding.container.VerticalContainer(\
            self, top=scr_top, \
            right=0, width=scr_width, \
            height=scr_height, left=1/2*self.width)

        self.desc_cont = pudding.container.VerticalContainer( \
            self, top=scr_top, left=self.width/2,\
            right=self.width/2, width=self.width/2, height=self.height/2)

        self.desc_label = pudding.control.SimpleLabel( \
                self.desc_cont, label='', autosize=True, \
                font=self.font_p, top=0, \
                left=0, color=self.color_p)



class SongEntry(SongEntryPresentation):
    def __init__(self, parent=None, width=0, height=0, top=0, left=0, right=0, \
            bottom=0, anchors=0, padding=0, song=None, start_screen=None, \
            song_manager=None, player=None, start_button_text='Enter'):
        SongEntryPresentation.__init__(self, parent=parent, \
            width=width, height=height, top=top, left=left, \
                right=right, bottom=bottom, anchors=anchors, \
                    padding=padding)

        self.song_manager = song_manager
        self.player = player
        self.song = song
        self.start_screen = start_screen
        self.l_artist = ""#'Artist: '
        self.l_title = ""#'Title: '
        self.l_description = ""#'Decription: '
        self.l_genre = str(_('Genre: '))
        self.l_edition = str(_('Edition: '))
        self.l_creator = str(_('Creator: '))
        self.l_bpm = str(_('BPM: '))
        self.l_start = start_button_text
        self.cover_loaded = False

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
        self.desc_label.label = desc
        if self.parent.use_pil:
            cover_path = self.get_cover()
            if cover_path:
                self.load_cover(cover_path)

        self.start_button.function = self.get_button_func()
        self.start_button.args = self.get_button_args()
        self.start_button.label = self.get_start_button_text()


    def show(self):
        self.visible=1
        self.on_resize()
        if self.parent.preview:
            self.player.load(self.song.path, self.song.info['mp3'])
            self.player.play()

    def hide(self):
        self.visible=0

    def load_cover(self, pic_path):
        import Image
        wanted_size = self.parent.width / 3.
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
            pil_image=pil_pic,\
            z_index=-3)
        self.cover_loaded = True

    def get_start_button_text(self):
        return self.l_start + ':  "' + self.song.info['title'] + '"'

    def get_cover(self):
        cover = None
        if 'cover' in self.song.info:
            cover = os.path.join(self.song.path, self.song.info['cover'])
        return cover

    def get_button_func(self):
        return self.start_start_screen

    def start_start_screen(self, args):
        self.parent.hide()
        self.start_screen.show(args)

    def get_button_args(self):
        return [self.song, self.parent]

    def stop_preview(self):
        self.player.pause()



class DirectoryEntryPresentation(CommonEntryPresentation):
    def __init__(self, parent=None, width=0, \
        height=0, top=0, left=0, right=0, \
        bottom=0, anchors=0, padding=0):
        CommonEntryPresentation.__init__(self, parent=parent,\
            width=width, height=height, top=top, left=left, right=right, \
                bottom=bottom, anchors=anchors, padding=padding)

        scr_top = self.height * 1 / 3
        scr_right = self.right
        scr_width = self.parent.screen_res_x
        scr_height = self.parent.screen_res_y
        self.cover_loaded = False
        self.cover_cont = pudding.container.VerticalContainer(\
            self, top=scr_top, \
            right=0, width=scr_width, \
            height=scr_height)
        self.cover_cont.left = 0

        self.desc_cont = pudding.container.VerticalContainer( \
            self, top=scr_top, left=self.width/3,\
            right=self.width/2, width=self.width/2, height=self.height/2)

        self.desc_label = pudding.control.SimpleLabel( \
                self.desc_cont, label='', autosize=True, \
                font=self.font_p, top=0, \
                left=0, color=self.color_p)




class DirectoryEntry(DirectoryEntryPresentation):
    def __init__(self, parent=None, width=0, height=0, top=0, left=0, right=0, \
            bottom=0, anchors=0, padding=0, name=None, start_screen=None, \
            song_manager=None, player=None):
        DirectoryEntryPresentation.__init__(self, parent=parent, \
            width=width, height=height, top=top, left=left, \
                right=right, bottom=bottom, anchors=anchors, \
                    padding=padding)
        self.name = name
        self.song_manager = song_manager
        self.entries = []
        self.current_entry = 0
        self.cover_loaded = False

    def append(self, obj):
        self.entries.append(obj)

    def show(self):
        self.start_button.label = self.get_start_button_text()
        self.start_button.args = self.get_button_args()
        self.start_button.function = self.get_button_func()
        self.desc_label.label = self.get_desc()
        if self.parent.use_pil:
            cover_path = self.get_cover()
            if cover_path:
                self.load_cover(cover_path)
        self.on_resize()
        self.visible=1

    def hide(self):
        self.visible=0

    def get_desc(self):
        desc = "Anzahl songs in Ordner: " + str(len(self.entries)) + '\n\n'
        if len(self.entries):
            desc += "Songs in there:" + '\n'
            for song in self.entries[:10]:
                if song.info['artist'] != "":
                    desc += song.info['artist'] + ' - '
                if 'title' in song.info:
                    desc += song.info['title'] + '\n'
            desc += '...'
        return desc

    def get_start_button_text(self):
        return "Enter" + ':  "' + "Directory >> " + self.name + '"' + '\n\n'

    def get_cover(self):
        app_dir = os.path.dirname(sys.argv[0])
        cover_path = os.path.join(app_dir, 'misc', 'directory.png')
        return cover_path

    def get_button_func(self):
        return self.song_manager.enter_sub_directory

    def get_button_args(self):
        return [self.name]

    def load_cover(self, pic_path):
        import Image
        wanted_size = self.parent.width / 3.
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
            pil_image=pil_pic,\
            z_index=-3)
        self.cover_loaded = True

    def stop_preview(self):
        pass

