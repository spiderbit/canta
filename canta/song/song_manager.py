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
from canta.song.song import Song, UltraStarFile

class SongManager:
    """Class to recursivly search, validate and sort a list of songs """

    def __init__(self, path):
        self.path = path
        self.songs = []

    def search(self):
        """Searches recursive ultrastar songs"""

        for entry in os.walk(self.path):
            root = entry[0]
            file_names = entry[2]
            for file_name in file_names:
                #file_name = file_name.decode('utf-8')
                lower_file = file_name.lower()
                if lower_file == "desc.txt":
                    pass
                elif lower_file.endswith('.txt'):
                    reader = UltraStarFile(root, file_name)
                    song = Song(path = root, reader=reader)
                    song.read(mode="headers")
                    file_names = unicode_encode_list(file_names)
                    self.songs.append(song)


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
    for elem in elements:
        try:
            new_list.append(elem.decode('utf-8', 'replace'))
        except UnicodeEncodeError:
            new_list.append(elem.decode('iso-8859-1'))
    return new_list
