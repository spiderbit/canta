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

import re
import sys
import time
import os
import codecs

from canta.song.song_segment import SongSegment
from canta.midi.MidiInFile import MidiInFile
from canta.midi.MidiOutFile import MidiOutFile
from canta.midi.MidiToTextFile import *
from song_line import SongLine

class Song:

	def __init__(self, title='', artist='', mp3 = None, path='', file='', bpm=0, gap=0, \
			start=0, line_nr=0, octave=False, debug=0):
		self.path = unicode(path, 'utf-8', errors='replace')		# only need this because i dont want break the api of coreinit and songmenu(browser) 
		self.file = file #unicode(file, 'utf-8', errors='replace')
		self.splitted = False
		self.debug = debug
		self.info = {}
		self.info['title'] = title
		self.info['artist'] = artist
		self.info['mp3'] = mp3
		self.info['bpm'] = bpm
		self.info['gap'] = gap
		self.info['start'] = start
		self.line_nr = line_nr
		self.pos = None
		self.end = False
		self.segments = []
		self.lines = []
		self.octave = octave
		

	def reset(self):
		self.line_nr = 0
		self.pos = None
		self.end = False


	def get_pos_in_segments(self, line_nr, pos):
		""" Finds segment position in song.segments

		Keyword arguments:
		line_nr -- the line_nr of song.line_nr
		pos -- pos in the line

		"""

		line = self.lines[line_nr]
		tone = line.segments[pos]
		seg_pos = self.segments.index(tone)
		return line, tone, seg_pos


	def split_in_lines(self):
		self.lines = []
		self.i = 0
		self.lines.append(SongLine(self.segments[0].time_stamp))
			
		for pos, segment in enumerate(self.segments):
			if segment.type == 'note':	# normal/special note
				self.lines[self.i].add_segment(segment)
			elif segment.type == 'pause':
				self.i = self.i + 1
				self.lines.append(SongLine(segment.time_stamp))
			elif segment.type == 'end':
				pass
					
		if self.debug:
			print "found ", len(self.lines), " lines"
			self.print_all_lines()

		self.splitted = True

		
	def print_all_lines(self):
		for i, line in enumerate(self.lines):
			print "<line nr=", i, " showTime=", line.show_time, " >"
			for x, segment in enumerate(line.segments):
				print " <element nr=", x, " pitch=", segment.pitch, ">"


	def getMinPitch(self):
		"""searches note with lowest pitch and returns it"""
		min = 100
		
		for segment in self.segments:
			if segment.type == 'note' and segment.pitch < min:
				min = segment.pitch
		return min


	def getMaxPitch(self):
		"""searches note with highest pitch and returns it"""
		max = 0
		for segment in self.segments:
			if segment.type == 'note' and segment.pitch > max:
				max = segment.pitch
		return max

	
	
	def read_from_us(self, us_file ='', type='segments'):	
		"""Parse a ultrastar-txt file and add header and segments to this object.

		Keyword arguments:
		us_file -- the Ultrastar file to parse
		type -- 'segments' | 'headers' | 'full' full is headers + segments  (default 'segments')

		"""

		if us_file == '':
			us_file = os.path.join(self.path, self.file)



		f = open(us_file,'r')
		sample = f.read(4)
		#if sample.startswith(codecs.BOM_UTF8):
		try:
			song_file = codecs.open(us_file, encoding="utf-8")
			song_lines = song_file.readlines()
		except UnicodeDecodeError:
			try:
				song_file = codecs.open(us_file, encoding="iso-8859-1")
				song_lines = song_file.readlines()
			except:
				song_file = codecs.open(us_file, encoding="cp437")
				song_lines = song_file.readlines()	
		
		for line in song_lines:
			line = line.replace('\r', '')
			line = line.replace('\n', '')

			if (type == "headers" or type == "full") and line.startswith('#'):
				words = line.strip('#').split(':')
				if len(words) == 2:
					if words[0] == 'BPM' \
						or words[0] == 'GAP' \
						or words[0] == 'START':

						self.info[words[0].lower()] \
							= float(words[1].strip().replace(',', '.'))
					elif words[0] == 'MP3':
						self.info[words[0].lower()] \
						    = words[1].strip()
					else:
						self.info[words[0].lower()] \
							= words[1].strip()
				else:
					print 'error: something wrong in the songfile:'\
						+ us_file, words
			elif type=="headers":       # that must accellerate header-parsing for song-browser on startup
				return

			elif type=="full" or type == "segments":
				self.parse_segment(line)
		self.convert_to_absolute()		

	def parse_segment(self, line):
		if line.startswith('-'):
			words = self.clean_string(line[1:].encode())
			if len(words) == 1:
				#print words
				self.addSegment(SongSegment( "pause", \
					float(words[0]), '', '', ''))
			elif len(words) == 2:
				self.addSegment(SongSegment( "pause", \
					float(words[1]), '', '', ''))
			else:
				print 'Song - readFile()-error: something wrong in the songfile:'\
					+ txtFile + words[0] + "blub" + words + line + line[1:]
				sys.exit()

		# Find out if the note is a
		#   : <- normal note
		#   * <- special note
		#   F <- freestyle note
		elif line.startswith(':') or line.startswith('*') or line.startswith('F'):
			#break
			words = self.clean_string(line[1:])
			tmp_list = []
			before_syllable = False
			syllable_found = False
			line_range = range(len(line))
			line_range.reverse()
			for i in line_range:
				#print "4", i, line[i]
				if line[i] == ' ':
					tmp_list.append(' ')
					if syllable_found:
						before_syllable = True
				else:
					if not before_syllable:
						tmp_list.append(line[i])
						syllable_found = True
					else:
						break

			tmp_list.reverse()
			text = ''.join(tmp_list[1:])
						
			special = False
			if line.startswith('*'):
				special = True # !!! That we should use something (*) ???
			freestyle = False
			if line.startswith('F'):
				freestyle = True
			time_stamp = int(words[0])
			duration = int(words[1])
			pitch = int(words[2])
			if not self.octave:
				pitch = pitch
				
			self.addSegment(SongSegment("note", \
						time_stamp, \
						duration, \
						pitch, \
						text, special, freestyle))

		elif line.startswith('E'):
			print line
			self.addSegment(SongSegment("end", \
				float(self.segments[-1].time_stamp), '', '', ''))




	def convert_to_absolute(self):
		if 'relative' in self.info and self.info['relative'].lower() == 'yes':
			if self.splitted:
				pass # join-lines??
			abs_line_start = 0
			for segment in self.segments:
				if segment.type == 'pause':
					abs_line_start = abs_line_start + segment.time_stamp
					segment.time_stamp = abs_line_start
				else:
					segment.time_stamp = abs_line_start + segment.time_stamp

					






	def read_from_midi(self, midi_file):
		"""Parse a midi file and fill with that data the SongSegment list.

		Keyword arguments:
		midi_file -- the midi file to parse
		
		"""
		
		f = open(midi_file, 'rb')

		# do parsing
		x = MidiToText(self)
		midiIn = MidiInFile(x, f)
		midiIn.read()
		f.close()

		

	def write_to_txt(self, txtFile = None):
		if txtFile == None:
			txtFile = os.path.join(self.path, self.file) 
		songFile = codecs.open(txtFile, encoding='utf-8', mode='w+')

		for key,value in self.info.iteritems():
			songFile.write(
				u'#' + \
					key.upper() + u':' \
					+ unicode(value) + u'\n'
				)
					

		
		for segment in self.segments:

			if segment.type == 'note':
				if segment.special:
					tmp = '*'
				else:
					tmp = ':'
				songFile.write(
					tmp + ' ' \
						+ str(segment.time_stamp) + ' ' \
						+ str(segment.duration) + ' ' \
						+ str(segment.pitch) + ' ' \
						+ segment.text + '\n'
					)
			elif segment.type == 'pause':
				songFile.write('- ' + str(segment.time_stamp) \
					+ '\n')
			elif segment.type == 'end':
				songFile.write('E')

	def addSegment(self, songSegment):
		self.segments.append(songSegment)


	def get_real_time(self, beats=1):   # this should be called or implemented in player?
		"""Calculates the position after x beats and in seconds

		Keyword arguments:
		beats -- amount of beats  (default 1)
		
		"""
		duration_of_one_beat = 1. /self.info['bpm'] *60# in seconds
		return (beats * duration_of_one_beat /  4) + (self.info['gap'] /1000.)


	def get_line_nr(self, time, old_line_nr = None):
		"""Searches line_nr of time in song

		Keyword arguments:
		time -- time in song in seconds
		old_line_nr -- optional last line-nr, a bit faster (experimental)
		
		"""
		end_line = len(self.lines)
		start_line = 0
		if old_line_nr == None:
			pass
		elif self.get_real_time(self.lines[old_line_nr].show_time) < time:
			start_line = old_line_nr
		else:
			end_line = old_line_nr
		
		for i,line in enumerate(self.lines[start_line:end_line]):
			last_segment = line.segments[len(line.segments)-1]
			if i+1 == end_line:
				if time > self.get_real_time(line.show_time):
					line_nr = i
					break
			
			elif i == 0 and time < self.get_real_time(self.lines[i+1].show_time):
				line_nr = 0
				break
			elif time < self.get_real_time(self.lines[i+1].show_time) \
			and	time > self.get_real_time(line.show_time):
				line_nr = start_line + i
				break
		else:
			line_nr = None
		return line_nr


	def get_pos(self, time, old_line_nr=None, old_tone_nr=None):
		"""Searches position of time in song returns line_nr, tone_nr

		Keyword arguments:
		time -- time in song in seconds
		old_line_nr -- optional last line-nr, a bit faster (experimental)
		old_tone_nr -- optional last tone-nr, a bit faster (experimental)
		
		"""
	
		tone_nr = None
		if old_line_nr == None:		# if i could not find a line i cannot find a tone_nr
			pos = None
		line_nr = self.get_line_nr(time = time, old_line_nr = old_line_nr)
		if line_nr == None:		# if i could not find a line i cannot find a tone_nr
			pos = None				# both None must be end of line or before gap was happend
		else:
			line = self.lines[line_nr]
			
			start_tone = 0
			end_tone = len(line.segments)
			if old_tone_nr == None:
				pass
			elif self.get_real_time(line.segments[old_tone_nr].time_stamp) >= time:
				start_tone = old_tone_nr
			else:
				end_tone = old_tone_nr
			
			for i,segment in enumerate(line.segments[start_tone:end_tone]):
				start = self.get_real_time(segment.time_stamp)
				end = self.get_real_time(segment.time_stamp + segment.duration)
				#print "start ", start,"end ", end,"time ", time
				if time > start:
					if time < end:
						tone_nr = i
						break
			#else:
			#		tone_nr = None
			#print "tone_nr ", tone_nr
		return line_nr, tone_nr






	def clean_string(self, parse_string):
		target_list = parse_string.split(' ')
		new_list = []
		for i, item in enumerate(target_list):
			if item == '' or item =='\r':
				pass
			else:
				new_list.append(target_list[i])
	
		return new_list



	def get_midi(self, line_nr, tone_nr):
		midi_tone = self.lines[line_nr].segments[tone_nr].pitch + 60 #72
		return midi_tone

	def get_freq(self, line_nr, tone_nr):
		
		midi_tone = self.get_midi(line_nr, tone_nr)
		freq = 440 * 2**(float(midi_tone-69)/12.)
		return freq
	
	
	# unused at the moment, but maybe we could use 
	# midi output of song or songparts so i let it stay for now
	def write_tone_to_midi(self, line_nr, tone_nr, out_file = 'midiout.mid'):
		"""Creates a midi file and write one tone to it

		Keyword arguments:
		line_nr  -- line_nr of the tone
		tone_nr  -- tone_nr in line
		out_file -- output midi file
		
		"""	
		midi = MidiOutFile(out_file)

		#format: 0, nTracks: 1, division: 480
		#----------------------------------
		#
		#Start - track #0
		#sequence_name: Type 0
		#tempo: 500000
		#time_signature: 4 2 24 8
		#note_on  - ch:00,  note:48,  vel:64 time:0
		#note_off - ch:00,  note:48,  vel:40 time:480
		#End of track
		#
		#End of file


		midi.header(0, 1, 480)
		
		midi.start_of_track()
		midi.sequence_name('Type 0')
		midi.tempo(int(60000000. / self.info['bpm']))
		midi.time_signature(4, 2, 24, 8)
		ch = 0
		i = 0
		midi.note_on(ch, self.lines[line_nr].segments[tone_nr].pitch+60, 0x64)
		midi.update_time(96*self.lines[line_nr].segments[tone_nr].duration)
		midi.note_off(ch, self.lines[line_nr].segments[tone_nr].pitch+60, 0x40)
		midi.update_time(0)
		
		midi.update_time(0)
		midi.end_of_track()
		
		midi.eof() # currently optional, should it do the write instead of write??


		midi.write()




	# unused at the moment, but maybe we could use 
	# midi output of song or songparts so i let it stay for now
	def write_line_to_midi(self, out_file = 'midiout.mid'):
		"""Creates a midi file and write current line to it"""	
		midi = MidiOutFile(out_file)

		#format: 0, nTracks: 1, division: 480
		#----------------------------------
		#
		#Start - track #0
		#sequence_name: Type 0
		#tempo: 500000
		#time_signature: 4 2 24 8
		#note_on  - ch:00,  note:48,  vel:64 time:0
		#note_off - ch:00,  note:48,  vel:40 time:480
		#End of track
		#
		#End of file


		midi.header(0, 1, 480)
		
		midi.start_of_track()
		midi.sequence_name('Type 0')
		midi.tempo(int(60000000. / self.info['bpm']))
		midi.time_signature(4, 2, 24, 8)
		ch = 0
		i = 0
		line = self.lines[self.line_nr]
		for i, segment in enumerate(line.segments[:-1]):	
			midi.note_on(ch, segment.pitch+60, 0x64)
			#96 is 4x midi clock which is one hole note
			midi.update_time(96 * segment.duration)
			midi.note_off(ch, segment.pitch+60, 0x40)
			midi.update_time(96	 * (line.segments[i+1].time_stamp - segment.time_stamp - segment.duration))
		
		midi.note_on(ch, line.segments[-1].pitch+60, 0x64)
		midi.update_time(96 * line.segments[-1].duration)
		midi.note_off(ch, line.segments[-1].pitch+60, 0x40)
		midi.update_time(0)
		midi.end_of_track()
		midi.eof() # currently optional, should it do the write instead of write??
		midi.write()


					


def main(): # main

	#need some code to make a song object first...

	song.addSegment(SongSegment( "note", 19, 5, 12, "hallo"))
	song.addSegment(SongSegment( "note", 24, 5, 33, "blub"))
	song.addSegment(SongSegment( "note", 29, 2, 69, "was"))
	song.addSegment(SongSegment( "note", 31, 5, 17, "geh-ht"))
	song.addSegment(SongSegment( "note", 39))
	song.addSegment(SongSegment( "note", 42, 5, 12, "es"))
	song.addSegment(SongSegment( "note", 47, 5, 6, "geht"))
	song.addSegment(SongSegment( "note", 52, 2, 2, "fast"))
	song.addSegment(SongSegment( "note", 54, 5, 3, "allet"))
	
	print "\n\n"
	
	print "Title:\t\t", song.title
	print "Artist:\t\t", song.artist
	print "AudioFile:\t", song.audioFile
	print "BPM:\t\t", song.bpm
	print "GAP:\t\t", song.gap, "\n"
	
	
	print "Type\t","TimeStamp\t","Duration\t","Pitch\t\t","Text\t\n\n"
	
	for segment in song.segments:
		
		print segment.type, "\t", segment.time_stamp, \
			"\t\t",segment.duration, "\t\t", \
			segment.pitch, "\t\t", segment.text
	
	print "\n\n"
	song.write_to_txt('Song.txt') 

if __name__ == '__main__': main()
