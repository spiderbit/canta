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
import sys
import soya
from threading import Thread

from canta.song.song import Song
from time import sleep
from time import time
import math


from canta.event.subjects.song_data import SongData
from canta.fft.fft_numpy import FFTNumPy
from canta.sound_manager.frequency_new import Frequency


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
		


	# that must in a big loop for events from the file from the
	# keyboard and from the microphone
	def run(self):
		selected_input = self.user_cfg.get_input()
		if selected_input == 'PyAudio':
			from canta.sound_manager.sound_manager_pyaudio import SoundManagerPyAudio
			sound_manager = SoundManagerPyAudio(sampling_frequency = 10000)
		else:
			from canta.sound_manager.sound_manager_oss import SoundManagerOSS
			sound_manager = SoundManagerOSS(sampling_frequency = 10000)

		sound_manager.start()
		numpy = FFTNumPy()
		freq = Frequency (sound_manager, numpy)
		# try to get better values with using midle-value
		
		#if(self.song_data.status != 'end'):
		while self.player.paused:
			sleep(0.05)
		while not self.song.end:			# song.player.stoped would be better
			if not self.player.paused:

				line_nr, tone_nr = self.song.get_pos(self.player.get_pos())
				#line_nr = self.song.get_line_nr(self.player.get_pos())
				#print line_nr, tone_nr
				
				if tone_nr != None:# and len(self.song.lines[self.song.line_nr].segments) < self.song.pos:
					target_pitch = self.song.lines[line_nr].segments[tone_nr].pitch
				else:
					sleep(0.01)
					continue
				#if not self.octave:
				#	target_pitch = abs(target_pitch) % 12

				timeBefore = self.player.get_pos()

				frequency = freq.get()
				if frequency is None:
					continue
				
				# Calculate the pitch.
				# We use the formula from MIDI standard and subtract 48 so
				# we match the Ultrastar conventions.
				# It works but I don't know why...

				self.pitch = 12. * math.log(frequency / 440., 2) + 69 - 48 #-48)#-24)#- 60)
				#print self.pitch
					
				if not self.octave:
					#self.pitch = self.pitch % 12
					
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

					if abs(difference) < 2:			# this is a help so that you only have to sing nearly right and get points
						self.pitch = target_pitch
					#else:
					#	print "bad pitches: ",self.pitch, target_pitch, difference
						#sys.exit(0)
				else:
					difference = self.pitch - target_pitch



				timeAfter = self.player.get_pos()
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
					#print self.msg['difference'], self.pitch, target_pitch

				sleep(0.01)

			else:
				#print "input.py: ich lebe noch"
				sleep(0.01)
		
		else:	# self.song.end
			#print "end??"
			sound_manager.stop()
		
	def stop(self):
		pass




