#! /usr/bin/python
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


import getopt
import pickle
import os, sys
from canta.song.song_manager import SongManager

x1 = os.path.join('tmp', 'song_compare.pkl')
x2 = 'tmp/new_file.pkl'

def dump_songs(dump_file_name, verbose=False):
    output_file = open(dump_file_name, 'wb')
    song_manager = SongManager(os.path.join('media', 'songs'))
    song_manager.search()
    song_manager.verify()
    songs = song_manager.songs
    if verbose:
        print "Testdump from %s songs" % len(songs)
    pickle.dump(songs, output_file, -1)
    output_file.close()

def pickle_songs(file_name):
    input_file = open(file_name, 'rb')
    songs = pickle.load(input_file)
    input_file.close()
    return songs

def test_compare():
    song_manager = SongManager(os.path.join('media', 'songs'))
    song_manager.search()
    song_manager.verify()
    song_manager.sort()
    print "Songs found:"
    print_song_stats(song_manager)
    songs = song_manager.songs
    testdata_songs = pickle_songs(x1)
    sm2 = SongManager(os.path.join('media', 'songs'))
    sm2.songs = testdata_songs
    print "Songs from compare-dump:"
    print_song_stats(sm2)
    assert songs == testdata_songs

def print_song_stats(song_manager):
    mp3s = song_manager.count_songs_with_attrib( 'mp3')
    covers = song_manager.count_songs_with_attrib( 'cover')
    print mp3s, " Songs with ", covers, " valid Covers found!"

usage="""
Usage:  %s [init]
    -i or --init < generates inital dump which will be compared with when you test it>
    - without parameter run the test
    """


if __name__ == '__main__':

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "hi", ["help", "init"])
    except getopt.GetoptError, err:
         # print help information and exit:
         print str(err) # will print something like "option -a not recognized"
         print usage
         sys.exit(2)


    if len(args) ==  0 and len(opts) == 0:
        test_compare()
        sys.exit()

    for o, a in opts:
        print o,a
        if o in ("-i", "--init"):
            dump_songs(x1, verbose=True)
            print "dumped to:", x1
        elif o in ("-h", "--help"):
            print usage
            sys.exit(2)
        else:
            assert False, "unhandled option"
