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


from threading import Thread

from canta.song.song import Song
from time import sleep
from time import time
import math
import sys, os

import pygst
pygst.require("0.10")
import gst
import pygtk, gtk, gobject

#from canta.event.subjects.song_data import SongData


spect_bands = 1024
AUDIOFREQ = 32000




class Input(Thread):
    def __init__(self, song=Song(), song_data=0, player=None, config=None):
        self.timeAfter = 0
        self.timeBefore = 0
        Thread.__init__(self)
        self.user_cfg = None
        self.player = player
        self.song_data = song_data

        self.paused = False # is the Song paused
        self.song = song # song data (class song)

        self.line_nr = -1

        # if its true i dont check for new song.events
        self.end_sended = False

        # i think the 4 is the resolution in the file
        # but i am not sure and 4 is default if nothing is given
        self.beat_time = 60. / song.info['bpm'] / 4
        self.pause_time = 0
        self.status = None
        self.switch_time = 0
        self.beat_time = 60. / song.info['bpm'] / 4

        self.current_note = None
        self.last_note = None

        self.octave = config['misc'].as_bool('octave_adjusting')

        self.tone_nr = None
        self.line_nr = None

        self.player_pipeline = gst.Pipeline("player")
        source = gst.element_factory_make("alsasrc", "audio-source")
        audiosink = gst.element_factory_make("fakesink", "audio-output")
        spectrum = gst.element_factory_make("spectrum", "my-spectrum")

        caps = gst.Caps ("audio/x-raw-int",rate=AUDIOFREQ)
        filter = gst.element_factory_make("capsfilter", "filter")
        filter.set_property("caps", caps)

        spectrum.set_property("bands", spect_bands)
        spectrum.set_property("threshold", -40)
        self.player_pipeline.add(source, spectrum, filter, audiosink)
        gst.element_link_many(source, spectrum, filter, audiosink)

        bus = self.player_pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)
        self.time = 0
        self.freq = None
        self.magnitude = None

    def run(self):
        #self.player_pipeline.get_by_name("audio-source").set_property("freq", 110)
        self.player_pipeline.set_state(gst.STATE_PLAYING)
        gtk.gdk.threads_init()
        gtk.main()


    def on_message(self, bus, message):
        self.msg = dict()
        t = message.type
        if t == gst.MESSAGE_EOS:
            pass
        elif t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            self.player_pipeline.set_state(gst.STATE_NULL)
        elif t == gst.MESSAGE_ELEMENT:
            if not self.player.get_pos():
                return
            timeBefore = self.timeAfter
            self.timeAfter = timeAfter = self.player.get_pos()
            self.msg['start_time'] = timeBefore
            self.msg['end_time'] = timeAfter

            magnitude = message.structure['magnitude']
            len_mag = len(magnitude)
            highest_mag = -40

            # TODO: checkout what's the difference between this time and timeAfter
            # and try to use this instead when possible, maybe there is starttime, too?
            self.time = message.structure['endtime']

            highest_mag_key = None
            for i in range(3, len_mag):
                if magnitude[i] > highest_mag:
                    highest_mag = magnitude[i]
                    highest_mag_key = i
            #highest_mag_key = 20
            if not highest_mag_key:
                frequency = pitch = None
            else:
                frequency = ((AUDIOFREQ / 2) * highest_mag_key + AUDIOFREQ / 4) / spect_bands * (32000 / AUDIOFREQ) * 1.37
                line_nr, tone_nr = self.song.get_pos(self.player.get_pos())

                # Calculate the pitch.
                # We use the formula from MIDI standard and subtract 48 so
                # we match the Ultrastar conventions.
                # It works but I don't know why...

                pitch = 12. * math.log(frequency / 440., 2) + 69 - 48 #-48)#-24)#- 60)

            if timeBefore != 'end' and timeAfter != 'end' \
                and timeBefore != 'pause' and timeAfter != 'pause':
                self.length = timeAfter - timeBefore
                self.length_in_beats = self.length / self.beat_time
                self.msg['type'] = "input"
                self.msg['pitch'] = pitch
                self.msg['song'] = self.song
                self.msg['real_pos_time'] = timeBefore - self.song.info['gap'] / 1000.
                self.msg['length_in_beats'] = self.length_in_beats
                self.msg['beat_time'] = self.beat_time
                self.song_data.set_data(self.msg) # round Event



    def stop(self):
        self.player_pipeline.set_state(gst.STATE_NULL)
        gtk.main_quit()
