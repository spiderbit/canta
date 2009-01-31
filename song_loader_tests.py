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
from canta.song import song_loader

x1 = os.path.join('tmp', 'song_compare.pkl')
x2 = 'tmp/new_file.pkl'

def dump_songs(dump_file_name, verbose=False):
    output_file = open(dump_file_name, 'wb')
    songs = song_loader.search_songs('songs')
    if verbose:
        print "Testdump from %s songs" % len(songs)
    pickle.dump(songs, output_file, -1)
    output_file.close()

def load_songs():
    input_file = open(dump_file_name, 'rb')
    #songs = song_loader.search_songs('songs')
    songs = pickle.load(input_file)
    input_file.close()
    return songs

def test_compare():
    #dumped_songs = load_songs()
    #songs = song_loader.search_songs('songs')
    dump_songs('tmp/new_file.pkl', verbose=True)
    import md5
    sum1 = md5.md5(open(x1,'rb').read()).digest()
    sum2 = md5.md5(open(x2,'rb').read()).digest()
    assert sum1 == sum2, "something went wrong"

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
