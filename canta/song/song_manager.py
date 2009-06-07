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

"""Module song_manager

a class and a few functions to find ultrastar songs and store it in a list
"""

import os
import sys
import soya.pudding as pudding

from canta.song.song import Song, UltraStarFile
from canta.directory import Directory
from canta.menus.menu import Menu
from canta.menus.button import MenuButton


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

        self.directory_cont = pudding.container.HorizontalContainer( \
            self, top=self.height * 0.02, \
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
        self.directory_up_button.function = self.song_manager.directory_up
        self.choose_base_button.function = self.parent.choose_base

    def show(self):
        self.visible=1
        self.choose_base_button.label = self.song_manager.name
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
        self.directory_up_button.function = self.song_manager.directory_up
        self.choose_base_button.function = self.parent.choose_base
        self.cover_loaded = False

    def append(self, obj):
        self.entries.append(obj)

    def show(self):
        self.start_button.label = self.get_start_button_text()
        self.start_button.args = self.get_button_args()
        self.start_button.function = self.get_button_func()
        self.choose_base_button.label = self.song_manager.name
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

class SongManager:
    """Class to recursivly search, validate and sort a list of songs """

    def __init__(self, parent_widget, directory, \
        sing_screen, player, name):
        self.directory = directory
        self.name = name
        self.songs = []
        self.sing_screen = sing_screen
        self.dir_pos = ''
        self.parent_widget = parent_widget
        self.player = player

    def clean_start(self, args):
        self.parent_widget.parent_widget.hide()
        self.stop_preview()
        if len(self.entries) > 0:
            self.start_screen.show(args)

    def stop_preview(self):
        if self.preview_sound:
            self.player.stop()

    def search(self):
        """Searches recursive ultrastar songs"""
        for entry in os.walk(self.directory.name):
            root = entry[0]
            file_names = entry[2]
            for file_name in file_names:
                lower_file = file_name.lower()
                if lower_file == "desc.txt":
                    pass
                elif lower_file.endswith('.txt'):
                    reader = UltraStarFile(root, file_name)
                    song = Song(directory = Directory(root), reader=reader)
                    song.read(mode="headers")
                    file_names = unicode_encode_list(file_names)
                    self.songs.append(song)
        self.browsable_items = self.get_entries(self.dir_pos)

    def get_entries(self, rel_path=None):
        root = Directory(self.directory.join(rel_path))
        entries = {}
        for song in self.songs:
            if song.directory.name.startswith(root.name):
                rel_depth = song.directory.get_depth() - \
                    root.get_depth()
                rel_path = song.directory.get_layer(root.name, 0)
                if rel_depth > 1:# and not rel_path in entries:
                    if rel_path not in entries:
                        entries[rel_path] = DirectoryEntry(\
                            parent=self.parent_widget, name=rel_path, \
                            start_screen=self.sing_screen, \
                            player=self.player, song_manager=self
                        )
                    if isinstance(entries[rel_path], DirectoryEntry):
                        entries[rel_path].entries.append(song)
                elif rel_depth == 1:
                    entries[rel_path] = SongEntry(\
                        parent = self.parent_widget, song = song, \
                        start_screen = self.sing_screen, \
                        player = self.player, song_manager=self,
                        start_button_text=self.parent_widget.song_start_text
                    )
        return entries

    def verify(self):
        """Verify the songs-list"""
        valid_picture_formats = ['jpg', 'jpeg', 'png']
        valid_sound_formats = ['ogg', 'mp3']
        cover_search_pattern = ['co']
        song_search_pattern = []
        remove_list = []
        for i in range(len(self.songs)):
            song = self.songs[i]
            file_names = []
            for entry in os.listdir(song.path):
                if os.path.isfile(os.path.join(song.path, entry)):
                    file_names.append(entry)
            self.__verify_song_item__(song, 'cover', \
                valid_picture_formats, file_names, cover_search_pattern)
            self.__verify_song_item__(song, 'mp3', valid_sound_formats, \
                file_names, song_search_pattern)
            if not __item_exist__(song, 'mp3'):
                remove_list.append(i)
        x = 0
        for i in remove_list:
            del self.songs[i - x]
            x += 1


    def __verify_song_item__(self, song, item, \
                valid_formats, file_names, patterns):
        '''Trys to verify/find the item with all availible magic'''
        # should be refactored
        tmp_file = False
        if __item_exist__(song, item) \
            and __item_exist_on_fs__(song, item):
            pass
        else:
            files = __files_with_right_format__(\
                valid_formats, song, file_names, item)
            files_count = len(files)
            if files_count > 1:
                for pattern in patterns:
                    tmp_file = __search_file_with_substring__(files, pattern)
                if not tmp_file:
                    tmp_file = __search_file_by_name__(
                        song.reader.file_name, files, valid_formats)
            elif files_count == 1:
                tmp_file = files[0]
            if tmp_file:
                song.info[item] = tmp_file


    def sort(self):
        """Sort songs by the pathnames"""
        self.songs.sort(key=lambda obj: obj.path + obj.info['mp3'])

    def count_songs_with_attrib(self, attr):
        """Counts songs which have the attr"""
        count = 0
        for song in self.songs:
            if attr in song.info:
                count += 1
        return count

    def select_entry(self, direction, pos=None):

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


    def directory_up(self):
        entry_pos_str = self.dir_pos.split('/')[-1]
        self.dir_pos = "/".join(self.dir_pos.split('/')[:-1])
        self.browsable_items = \
            self.get_entries(self.dir_pos)
        entry_pos = self.browsable_items.keys().index(entry_pos_str)
        self.parent_widget.reload_view('set_pos', entry_pos)

    def enter_sub_directory(self, args):
        self.dir_pos = os.path.join(self.dir_pos, args[0])
        self.enter_directory(0)

    def enter_directory(self, pos):
        self.browsable_items = self.get_entries(self.dir_pos)
        self.parent_widget.reload_view('set_pos', pos)

def __search_file_by_name__(file_name, files, valid_formats):
    """Search file with name=file_name but extention from valid_formats list"""
    name = remove_extention(file_name)
    for format in valid_formats:
        for file_name in files:
            if (name + '.' + format).upper() == file_name.upper():
                return file_name

def __item_exist__(song, check_item):
    """Check for existence of element in song.info and on the filesystem"""
    if check_item in song.info and \
        song.info[check_item] != None:
        return True
    else:
        return False

def __files_with_right_format__(valid_formats, song, file_names, check_item):
    """Returns a list of files with the right format in the directory"""
    # should be refactored
    found = False
    files_with_right_format = []
    for format in valid_formats:
        if __item_exist__(song, check_item):
            item = remove_extention(song.info[check_item]) \
                + "." + format
        for file_name in file_names:
            if __item_exist__(song, check_item) \
                and item.lower() == file_name.lower():
                found = True
                files_with_right_format.append(file_name)
                break
            elif file_name.lower().endswith(format):
                files_with_right_format.append(file_name)
        if found:
            break
    return files_with_right_format


def __search_file_with_substring__(files_with_right_format, substring):
    """Try to find a file with substring in name"""
    for file_name in files_with_right_format:
        if (file_name.lower()).find(substring.lower()) != -1:
            return file_name
    else:
        return False


def find_double_songs(songs):
    """find song objects with the same path"""
    # known bug all hits are double (x:y) and (y:x)
    for song_x in songs:
        for song_y in songs:
            if song_x.path == song_y.path and song_x != song_y:
                print "x:", song_x.path, song_x.info['mp3']
                print "y:", song_y.path, song_y.info['mp3']

def __last_path_part__(path):
    """Return the last part of a path"""
    # unused at the moment
    return path.split(os.path.sep)[-1]

def __item_exist_on_fs__(song, item):
    """Check for existence of item on filesystem"""
    return os.path.exists(song.path + song.info[item])

def remove_extention(file_name):
    """Remove last extention from a filename-string"""
    file_name_parts = file_name.split('.')
    return '.'.join(file_name_parts[:-1])


def unicode_encode_list(elements):
    """encode each string in a string-list to unicode"""
    new_list = []
    encodings = ['utf-8', 'iso-8859-1']
    for elem in elements:
        for enc in encodings:
            new_elem=decoder(elem, enc)
            if new_elem:
                new_list.append(new_elem)
                break
        else:
            new_list.append(elem)
    return new_list


def decoder(elem, coding):
    try:
        elem.decode(coding, 'replace')
        return elem
    except UnicodeEncodeError:
        return False

