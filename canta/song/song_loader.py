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

"""Module song_loader

functions to find the ultrastar song-directorys
"""

import os
from canta.song.song import Song, UltraStarFile


def search_songs(songs_path):
    """Searches recursive for valid ultrastar songs
        and returns it in a list

    A valid ultrastar-song is a Directory with at least:
        - one textfile in the ultrastar format
        - one ogg/mp3 music file
    """
    songs = []
    for entry in os.walk(songs_path):
        root = entry[0]
        file_names = entry[2]

        for file_name in file_names:
            #file_name = file_name.decode('utf-8')
            valid_picture_formats = ['jpg', 'jpeg', 'png']
            valid_sound_formats = ['ogg', 'mp3']
            lower_file = file_name.lower()
            if lower_file == "desc.txt":
                pass
            elif lower_file.endswith('.txt'):
                reader = UltraStarFile(root, file_name)
                song = Song(path = root, reader=reader)
                song.read(mode="headers")
                file_names = unicode_encode_list(file_names)
                __verify_stuff__(song, 'cover', \
                    valid_picture_formats, file_names)
                __verify_stuff__(song, 'mp3', valid_sound_formats, file_names)
                if __item_exist__(song, 'mp3'):
                    songs.append(song)

    #mp3s = __count_songs_with_attrib__(songs, 'mp3')
    #covers = __count_songs_with_attrib__(songs, 'cover')
    #print mp3s, " Songs with ", covers, " valid Covers found!"
    songs = __sort_songs_by_path_and_mp3__(songs)
    return songs


def __verify_stuff__(song, item, valid_formats, file_names):
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
            tmp_file = __search_file_by_bogos__(files, item)
        elif files_count == 1:
            tmp_file = files[0]
    if tmp_file:
        song.info[item] = tmp_file
        tmp_file = False


def __item_exist__(song, check_item):
    """Check for existence of element in song.info and on the filesystem"""
    if check_item in song.info and \
        song.info[check_item] != None:
        return True


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


def __search_file_by_bogos__(files_with_right_format, check_item):
    """Try to find file with co string
    ! many covers have this in the filename !
    """
    for file_name in files_with_right_format:
        # bad hack but the covers have often a substring [CO]
        if (file_name.lower().find(check_item)) != -1 \
                or (file_name.lower()).find("co") != -1:
            return file_name
    else:
        return False


def __count_songs_with_attrib__(songs, attr):
    """Counts songs which have the attr"""
    count = 0
    for song in songs:
        if attr in song.info:
            count += 1
    return count


def __sort_songs_by_path_and_mp3__(songs):
    """Sort song-list by the pathnames"""
    songs.sort(key=lambda obj: obj.path + obj.info['mp3'])
    return songs

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
