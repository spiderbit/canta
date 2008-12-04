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
	def __init__(self, song=Song(), song_data=0, player=None, octave=False, debug=0):
		
		Thread.__init__(self)
		self.msg = dict()
		self.user_cfg = None
		self.player = player
		self.debug = debug
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
		
		self.octave = octave

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
		t = message.type
		if t == gst.MESSAGE_EOS:
			pass
		elif t == gst.MESSAGE_ERROR:
			err, debug = message.parse_error()
			print "Error: %s" % err, debug
			self.player_pipeline.set_state(gst.STATE_NULL)
		elif t == gst.MESSAGE_ELEMENT:
			magnitude = message.structure['magnitude']
			len_mag = len(magnitude)
			highest_mag = -40
			self.time = message.structure['endtime']
			highest_mag_key = None
			for i in range(3, len_mag):
				if magnitude[i] > highest_mag:
					highest_mag = magnitude[i]
					highest_mag_key = i
			if not highest_mag_key:
				return
			freq = ((AUDIOFREQ / 2) * highest_mag_key + AUDIOFREQ / 4) / spect_bands * (32000 / AUDIOFREQ) * 1.37
			line_nr, tone_nr = self.song.get_pos(self.player.get_pos())
			
			if tone_nr != None:# and len(self.song.lines[self.song.line_nr].segments) < self.song.pos:
				target_pitch = self.song.lines[line_nr].segments[tone_nr].pitch
			else:
				sleep(0.01)
				return None
				
			timeBefore = self.player.get_pos()

			frequency = freq
			if frequency is None:
				return None	
			
			# Calculate the pitch.
			# We use the formula from MIDI standard and subtract 48 so
			# we match the Ultrastar conventions.
			# It works but I don't know why...

			self.pitch = 12. * math.log(frequency / 440., 2) + 69 - 48 #-48)#-24)#- 60)

			if not self.octave:	
				same_octave = False
				while not same_octave:			# that code do all tones display on same octave
					difference = self.pitch - target_pitch
					if difference > 6:
						self.pitch -= 12
					elif difference < -6:
						self.pitch += 12
					else:
						same_octave = True

				difference = self.pitch - target_pitch

				# this is a help so that you only
				#have to sing nearly right and get points
				if abs(difference) < 2:
					self.pitch = target_pitch
				#else:
				#	print "bad pitches: ",self.pitch, target_pitch, difference
					#sys.exit(0)
			else:
				difference = self.pitch - target_pitch

			timeAfter = self.player.get_pos()
			timeBefore = timeAfter -0.1
			if timeAfter != "pause" and timeBefore != "pause" and \
				timeBefore != "end" and timeAfter != "end":
				self.length = timeAfter - timeBefore
				self.length_in_beats = self.length / self.beat_time
				self.msg['type'] = "input"
				self.msg['pitch'] = self.pitch
				self.msg['song_pitch'] = target_pitch
				self.msg['difference'] = abs(self.pitch - target_pitch )
				self.msg['song'] = self.song
				self.msg['real_pos_time'] = timeBefore - self.song.info['gap'] / 1000.
				self.msg['length_in_beats'] = self.length_in_beats
				self.msg['beat_time'] = self.beat_time
				if line_nr != None:
					self.song_data.set_data(self.msg) # round Event



	def stop(self):
		self.player_pipeline.set_state(gst.STATE_NULL)




		

		


