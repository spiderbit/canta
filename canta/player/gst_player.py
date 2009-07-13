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

import sys, os
import pygst
pygst.require("0.10")
import gst

from player import Player

class GSTPlayer(Player):

    def __init__(self, path=None, file=None, time=0.0):
        Player.__init__(self, path, file, time)
        self.playbin = gst.element_factory_make("playbin", "player")
        self.clock = None
        self.pipeline = gst.Pipeline("mypipeline")
        self.audiotestsrc = gst.element_factory_make("audiotestsrc", "audio")
        self.pipeline.add(self.audiotestsrc)
        sink = gst.element_factory_make("autoaudiosink", "sink")
        self.pipeline.add(sink)
        self.audiotestsrc.link(sink)
        self.time_format = gst.Format(gst.FORMAT_TIME)
        bus = self.playbin.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)
        self.ended = False


    def load(self, path=None, file=None):
        self.loaded = True
        if path != None:
            self.path=path
        if file != None:
            self.file=file
        filepath = os.path.abspath(os.path.join(self.path, self.file))
        self.playbin.set_state(gst.STATE_NULL)
        self.playbin.set_property("uri", "file://" + filepath)
        self.clock = self.playbin.get_clock()

    def stop(self):
        self.playbin.set_state(gst.STATE_NULL)

    def play(self, start=0):
        self.ended = False
        if not self.paused and start!=0:
            result = self.playbin.set_state(gst.STATE_PAUSED)
            self.playbin.get_state() # block until the state is really changed
            seek_ns = start * 1000000000
            self.playbin.seek_simple(self.time_format, gst.SEEK_FLAG_FLUSH, seek_ns)
        self.playbin.set_state(gst.STATE_PLAYING)
        self._play()

    def is_paused(self):
        """
            Returns True if the player is currently paused
        """
        return self._get_gst_state() == gst.STATE_PAUSED

    def _get_gst_state(self):
        """
            Returns the raw GStreamer state
        """
        return self.playbin.get_state(timeout=50*gst.MSECOND)[1]

    def get_pos(self):
        state = self.playbin.get_state(timeout=50*gst.MSECOND)[1]
        if self.is_paused():
            return "pause"
        elif self.ended:
            #self.ended = False
            return "end"
        elif state == gst.STATE_PLAYING:
            try:
                duration, format = self.playbin.query_duration(gst.FORMAT_TIME)
                pos = self.playbin.query_position(gst.FORMAT_TIME)[0]
                if pos < duration:
                    return pos / 1000000000.
            except gst.QueryError:
                return 0
        else:
            # catch some states like READY (others?)
            return None

    def get_duration(self):
        """Returns the duration of the song in seconds"""
        duration, format = self.playbin.query_duration(gst.FORMAT_TIME)
        return duration / 1000000000.

    def pause(self):
        self.playbin.set_state(gst.STATE_PAUSED)
        self._pause()

    def play_freq(self, freq):
        self.audiotestsrc.set_property("freq", freq)
        self.pipeline.set_state(gst.STATE_PLAYING)

    def stop_freq(self):
        self.pipeline.set_state(gst.STATE_NULL)

    def fadeout(self):
        print "not implemented yet"

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.playbin.set_state(gst.STATE_NULL)
            self.ended=True
        elif t == gst.MESSAGE_ERROR:
            self.playbin.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            #print "Error: %s" % err, debug



def main():
    x = GSTPlayer()
    if len(sys.argv) > 1:
        f = sys.argv[1]
    else:
        print "Usage:  %s [OPTION]... [FILE]" % (sys.argv[0])
        sys.exit()
    x.load('', f)
    x.play()
    raw_input('hit key to pause')
    x.pause()
    print "pause at: ", x.get_pos()
    raw_input('hit a key to unpause')
    x.play()
    raw_input('hit a key to stop')
    x.stop()

if __name__ == '__main__': main()

