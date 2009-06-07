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

from canta.song.song import Song, UltraStarFile
from canta.directory import Directory
from canta.menus.browser_entry import *


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

