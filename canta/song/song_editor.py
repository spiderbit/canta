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
import time
import os
import thread
import soya
import soya.pudding as pudding

from canta.event.observers.song_label_observer import SongLabelObserver
from canta.event.observers.main_cube_observer import MainCubeObserver
from canta.event.observers.click_observer import ClickObserver
from canta.event.observers.lyrics_bg_box import LyricsBgBox
from canta.event.subjects.song_data import SongData
from canta.song.song import Song
from canta.menus.menu import Menu
from canta.menus.button import MenuButton
from canta.menus.text import MenuText
from canta.menus.input_field import InputField
from canta.event.keyboard_event import KeyboardEvent
from canta.event.song_event import SongEvent
from canta.song.song_segment import SongSegment




class SongEditor(soya.Body):
	"""TODO...
	"""
	def __init__(self, app_dir, widget_properties, theme_mgr, main_menu, player, debug=0):


		self.l_help_hint_0 = _(u'Press [h] for help...')
		self.l_help_hint_1 = _(u'Press [ESC] to go back...')
		self.l_help_hint = self.l_help_hint_0
		self.l_bpm = _(u'BPM: ')
		self.l_line_no = _(u'Line: ')
		self.separator = u' - '
		self.h_help = _(u'Help')
		self.help_file_path = os.path.join(app_dir, 'media', 'HELP.txt')
		self.debug = debug
		self.widget_properties = widget_properties
		self.app_dir = app_dir
		self.parent_world = widget_properties['root_world']
		self.parent_widget = widget_properties['root_widget']
		self.theme_mgr = theme_mgr

		self.screen_res_x = self.widget_properties['config']['screen'].as_int('resolution_x')
		self.screen_res_y = self.widget_properties['config']['screen'].as_int('resolution_y')

		self.font_p = widget_properties['font']['p']['obj']
		self.color_p = widget_properties['font']['p']['color']

		self.font_h = widget_properties['font']['h1']['obj']
		self.color_h = widget_properties['font']['h1']['color']

		self.main_menu = main_menu
		# A container for the heading label:
		self.v_cont = pudding.container.VerticalContainer( \
				self.parent_widget, left=20, top=20)
		self.v_cont.padding = 15
		self.v_cont.anchors = pudding.ANCHOR_TOP | pudding.ANCHOR_LEFT
		self.v_cont.visible = 0

		self.help_hint_cont = pudding.container.VerticalContainer( \
				self.parent_widget, left=self.screen_res_x / 2.5, top=5)
		self.help_hint_cont.right = 10
		self.help_hint_cont.anchors = pudding.ANCHOR_ALL
		self.help_hint_cont.visible = 0
		self.keyboard_event = KeyboardEvent(self.widget_properties, \
				 self.debug, theme_mgr)

		self.tone_txt_input = InputField(self.widget_properties, '')
		self.tone_txt_input.label.visible = 0
		
		self.player = player
		self.connect_keys()
		self.msg = dict()


	def show(self, args):
		for item in args[1]:
		    item.visible = 0

		# get name of the selected song name from args:
		self.selected_song = args[0].info['mp3']
		self.song = args[0]
		self.v_cont.visible = 1
		self.setup()


	def setup(self):
		# Sizes and positions for the lyrics:
		pos_size = {}
		pos_size['width'] = 70
		pos_size['height'] = 30
		pos_size['top'] = self.widget_properties['config']['screen'].as_int('resolution_y') / 1.1 - 12
		pos_size['left'] = 35
		self.widget_properties['pos_size'] = pos_size
		self.widget_properties['anchoring'] = 'bottom'

		# We deactivate the "done"-color by giving it the same color as "to_sing":
		self.lyrics_to_sing_color = self.widget_properties['font']['lyrics']['to_sing']['color']
		self.widget_properties['font']['lyrics']['to_sing']['color'] = \
			self.widget_properties['font']['lyrics']['done']['color']

		# The observer for the lyrics:
		lyrics = SongLabelObserver(self.widget_properties, self.debug)

		# The observer for the symbolical musical representations:

		song_bar_color = {}
		song_bar_color['special'] = (1, 0, 0, 0.6)
		song_bar_color['freestyle'] = (0, 1., 0., 0.6)
		song_bar_color['normal'] = (0, 0., 1., 0.4)

		cube = MainCubeObserver(self.widget_properties['root_world'], \
						song_bar_color, self.debug)
		# The observer for the background box (lyrics):
		l_bg_box = LyricsBgBox(self.widget_properties, self.debug)

		self.pos = 0
		self.song_data = SongData()
		self.song_data.attach(lyrics)
		self.song_data.attach(l_bg_box)
		self.song_data.attach(cube)

		# The paths to the song:
		self.msg['song'] = self.song
		self.song.read_from_us()
		self.song.split_in_lines()
		self.msg['type'] = 'nextLine'
		self.song_data.set_data(self.msg)
		self.msg['pos'] = 0
		self.msg['type'] = 'activateNote'
		self.song_data.set_data(self.msg)

		self.player.load(path=self.song.path, file= self.selected_song)

		self.heading_label = pudding.control.SimpleLabel( \
				self.v_cont, label=self.song.info['artist'] + \
				self.separator + self.song.info['title'], \
				font=self.font_h,\
				color=self.color_h, top=10, left=0)

		# The line number label:
		ln_label = ''
		self.line_number_label = pudding.control.SimpleLabel( \
			self.v_cont, label=ln_label, font=self.font_p, \
			color=self.color_p)

		self.bpm_label = self.l_bpm + str(self.song.info['bpm'])
		self.bpm_number_label = pudding.control.SimpleLabel( \
			self.v_cont, label= self.bpm_label, font=self.font_p, \
			color=self.color_p)

		self.parent_widget.on_resize()
		self.parent_world.add(self.keyboard_event)

		# Help menu:
		self.help_menu = MenuText(self.widget_properties, top=self.screen_res_y / 5, \
				left=self.screen_res_x / 2)
		self.help_menu.set_heading(self.h_help)
		fd_help = open(self.help_file_path, 'r')  
		help = fd_help.read()
		self.help_menu.add_text(help)
		self.help_menu.text_cont.visible = 0
		self.help_hint = pudding.control.SimpleLabel(self.help_hint_cont, \
				label=self.l_help_hint)

		self.help_hint_cont.visible = 1
		
		click_observer = ClickObserver(click_sound=os.path.join(self.app_dir, 'click.wav'))
		self.song_data2 = SongData()
		self.song_data2.attach(click_observer)

		self.parent_widget.on_resize()
		self.refresh()

	def back(self):
		self.msg['type'] = 'end'

		self.song_data.set_data(self.msg)

		del self.v_cont.children[0:]
		del self.help_hint_cont.children[0:]
		self.help_menu.box_cont.visible = 0
		self.help_hint_cont.visible = 0
		self.parent_world.remove(self.keyboard_event)
		# We reactivate the "done"-color:
		self.widget_properties['font']['lyrics']['to_sing']['color'] = \
			self.lyrics_to_sing_color
		self.quit_help()
		self.main_menu.show()


	def help(self):
		self.msg['type'] = 'nextLine'
		self.song_data.set_data(self.msg)
		
		self.keyboard_event.reset()
		self.keyboard_event.add_connection(type = soya.sdlconst.K_q, \
			action = self.back)
		self.keyboard_event.add_connection(type = soya.sdlconst.K_ESCAPE, \
			action = self.quit_help)
		self.keyboard_event.add_connection(type = soya.sdlconst.K_h, \
			action = self.quit_help)
		self.heading_label.visible = 0
		self.line_number_label.visible = 0
		self.bpm_number_label.visible = 0
		self.help_menu.text_cont.visible = 1
		self.help_menu.box_cont.visible = 1
		self.help_hint.label = self.l_help_hint_1


	def quit_help(self):
		self.heading_label.visible = 1
		self.line_number_label.visible = 1
		self.bpm_number_label.visible = 1
		self.keyboard_event.reset()
		self.connect_keys()
		self.help_hint.label = self.l_help_hint_0
		self.help_menu.text_cont.visible = 0			
		self.help_menu.box_cont.visible = 0
		self.refresh()


	def init_text_field(self):
		self.tone_txt_input.label.value = self.song.lines[self.song.line_nr].segments[self.pos].text
		self.tone_txt_input.label.visible = 1
		self.tone_txt_input.post_method = self.end_change_text
		
	def change_text(self):
		self.init_text_field()
		self.parent_world.remove(self.keyboard_event)

		self.parent_world.add(self.tone_txt_input)
		

	def end_change_text(self):
		if self.tone_txt_input.done:
			self.song.lines[self.song.line_nr].segments[self.pos].text = self.tone_txt_input.label.value
		self.tone_txt_input.label.visible = 0
		self.parent_world.remove(self.tone_txt_input)
		self.parent_world.add(self.keyboard_event)
		self.refresh()

	def split_line(self):
		line, tone, seg_pos = self.song.get_pos_in_segments(self.song.line_nr, self.pos)
		if self.song.segments > seg_pos+1 and self.pos < len(line.segments)-1:
			self.song.segments.insert(seg_pos+1, SongSegment( "pause", self.get_next_pos(tone)))
			self.song.split_in_lines()
		self.refresh()


	def get_next_pos(self, tone):
		''' returns pos of next free position for a element after the actual tone
		'''
		return tone.time_stamp+tone.duration+1

	def merge_lines(self):
		line, tone, seg_pos = self.song.get_pos_in_segments(self.song.line_nr, self.pos)
		if self.song.line_nr + 1 < len(self.song.lines):
			for segment in self.song.segments[seg_pos:]:
				if segment.type == 'pause':
					self.song.segments.pop(self.song.segments.index(segment))
					break
			self.refresh()
		elif self.song.line_nr + 1 == len(self.song.lines) and self.song.line_nr > 0:
			self.song.line_nr -= 1
			self.merge_lines()
		

	def add_tone(self):
		line, tone, seg_pos = self.song.get_pos_in_segments(self.song.line_nr, self.pos)
		self.song.segments.insert(seg_pos+1, SongSegment( "note", self.get_next_pos(tone), 1, tone.pitch, text = '-'))
		self.refresh()

	def rem_tone(self):
		line, tone, seg_pos = self.song.get_pos_in_segments(self.song.line_nr, self.pos)
		
		line_nr = self.song.line_nr
		number_of_segments = len(self.song.lines[line_nr].segments)
		number_of_lines = len(self.song.lines)
		if number_of_segments == 1:
			if line_nr > 0:
				self.song.segments.pop(seg_pos)
				self.song.line_nr -= 1
				self.merge_lines()
			elif line_nr == 0 and number_of_lines > 1:
				self.merge_lines()
				self.song.segments.pop(seg_pos)
			else:
				pass
				#print "you cant delete last segment in last line"
				
		else:	
			self.song.segments.pop(seg_pos)
			if self.pos + 1 == number_of_segments:
				self.pos -= 1
		self.refresh()

	def play_tone_wave(self):
		start_tone = self.song.lines[self.song.line_nr].segments[self.pos]
		self.play_wave(start_tone)
	
	def play_wave(self, start_tone, end_tone = None):
		duration_of_one_beat = 1. /self.song.info['bpm'] * 60
		if end_tone == None:
			end_tone = start_tone
		beats = end_tone.duration + end_tone.time_stamp - start_tone.time_stamp
		length = beats * duration_of_one_beat / 4
		start = self.song.get_real_time(start_tone.time_stamp)
		self.player.play(start=float (start))
		time.sleep(length)
		self.player.stop()

	def play_line_wave(self):
		start_tone = self.song.lines[self.song.line_nr].segments[0]
		end_tone = self.song.lines[self.song.line_nr].segments[-1]
		self.play_wave(start_tone, end_tone)

	def play_tone_both(self):
		thread.start_new_thread(self.play_tone_freq, () )
		thread.start_new_thread(self.play_tone_wave, () )
		
	def play_line_both(self):
		thread_id = thread.start_new_thread(self.play_line_wave,())
		#if thread_id == thread.get_ident():
		#	thread.exit()
		thread.start_new_thread(self.play_line_freq, () )

	def play_tone_freq(self):
		self.play_freq(self.song.line_nr, self.pos)

	def play_line_freq(self):
		line = self.song.lines[self.song.line_nr]
		for i, segment in enumerate(line.segments[:-1]):
			b = time.time() 
			self.play_freq(self.song.line_nr, i)
			dur = time.time() - b
			sleep_time = (line.segments[i+1].time_stamp - (segment.time_stamp)) * \
			    (1. /self.song.info['bpm'] *60.)/4.-dur
			if sleep_time > 0:
				time.sleep(sleep_time)
		self.play_freq(self.song.line_nr, len(line.segments)-1)
		
	def play_freq(self, line_nr, note_nr):
		note = self.song.lines[line_nr].segments[note_nr]
		duration = note.duration* (1. /self.song.info['bpm'] *60) / 4
		freq = self.song.get_freq(line_nr, note_nr)
		self.player.play_freq(freq)
		time.sleep(duration)
		self.player.stop_freq()

	def bpm_up(self):
		self.song.info['bpm'] += 1
		self.bpm_number_label.label = u'BPM: '+ str(self.song.info['bpm'])

	def bpm_min(self):
		self.song.info['bpm']-=1
		self.bpm_number_label.label = u'BPM: '+ str(self.song.info['bpm'])


	def next(self):
		self.pos = 0
		if self.song.line_nr + 1 < len(self.song.lines):
			self.song.line_nr += 1
		else:
			self.song.line_nr = 0
		self.refresh()

	def refresh(self):
		self.song.split_in_lines()
		self.msg['type'] = 'nextLine'
		self.song_data.set_data(self.msg)
		self.msg['pos'] = self.pos
		self.msg['type'] = 'activateNote'
		self.song_data.set_data(self.msg)
		self.line_count = str(len(self.song.lines))
		self.line_number_label.label = self.l_line_no \
			+ str(self.song.line_nr + 1) + u' / ' \
			+ self.line_count	


	def prev(self):
		self.pos = 0
		if self.song.line_nr > 0:
			self.song.line_nr -= 1
		else:
			self.song.line_nr = len(self.song.lines) - 1
		self.refresh()


	def select_note(self, args):
		self.msg['type'] = 'deActivateNote'
		self.msg['old_pos'] = self.pos
		self.song_data.set_data(self.msg)
		if args =='next':
			if self.pos < len(self.song.lines[self.song.line_nr].segments) - 1:
				self.pos += 1
		elif self.pos > 0:
			self.pos -= 1
		self.refresh()

	def increase(self):
		self.song.lines[self.song.line_nr].segments[self.pos].duration += 1
		self.refresh()

	def minimize(self):
		if self.song.lines[self.song.line_nr].segments[self.pos].duration >= 1:
			self.song.lines[self.song.line_nr].segments[self.pos].duration -= 1
			self.refresh()

	def save(self):
		self.song.write_to_txt()


	def move(self, dif):
		self.song.lines[self.song.line_nr].segments[self.pos].time_stamp += dif
		self.refresh()

	def move_ri(self):
		line, tone, seg_pos = self.song.get_pos_in_segments(self.song.line_nr, self.pos)
		self.move(1)
		if self.pos + 1 < len(line.segments):
			if tone.time_stamp > line.segments[self.pos + 1].time_stamp:  # if tone have later timestamp then next tone, switch position in list
				next_tone = line.segments[self.pos + 1]
				self.song.segments[seg_pos] = next_tone
				self.song.segments[seg_pos + 1] = tone
				self.pos = self.pos + 1
				self.refresh()
		

	def move_le(self):
		line, tone, seg_pos = self.song.get_pos_in_segments(self.song.line_nr, self.pos)
		self.move(-1)
		if self.pos > 0:
			if tone.time_stamp < line.segments[self.pos - 1].time_stamp:  # if tone have further timestamp then the tone before, switch position in list
				before_tone = line.segments[self.pos - 1]
				self.song.segments[seg_pos] = before_tone
				self.song.segments[seg_pos - 1] = tone
				self.pos = self.pos - 1
				self.refresh()
				

	def change_pitch(self, dif):
		self.song.lines[self.song.line_nr].segments[self.pos].pitch += dif
		self.refresh()

	def pitch_up(self):
		self.change_pitch(1)	


	def pitch_down(self):
		self.change_pitch(-1)



	def connect_keys(self):
		self.keyboard_event.add_connection(type = soya.sdlconst.K_q, \
			action = self.back)	
		self.keyboard_event.add_connection(type = soya.sdlconst.K_PAGEDOWN, \
			action = self.prev)
		self.keyboard_event.add_connection(type = soya.sdlconst.K_PAGEUP, \
			action = self.next)		
		self.keyboard_event.add_connection(type = soya.sdlconst.K_LEFT, \
			action = self.select_note, args = 'prev')
		self.keyboard_event.add_connection(type = soya.sdlconst.K_RIGHT, \
			action = self.select_note, args = 'next')
		self.keyboard_event.add_connection(type = soya.sdlconst.K_PLUS, \
			action = self.increase)
		self.keyboard_event.add_connection(type = soya.sdlconst.K_MINUS, \
			action = self.minimize)
		self.keyboard_event.add_connection(type = soya.sdlconst.K_KP_PLUS, \
			action = self.increase)
		self.keyboard_event.add_connection(type = soya.sdlconst.K_KP_MINUS, \
			action = self.minimize)	
		self.keyboard_event.add_connection(type = soya.sdlconst.K_s, \
			action = self.save)
		self.keyboard_event.add_connection(type = soya.sdlconst.K_y, \
			action = self.move_le)
		self.keyboard_event.add_connection(type = soya.sdlconst.K_x, \
			action = self.move_ri)		
		self.keyboard_event.add_connection(type = soya.sdlconst.K_UP, \
			action = self.pitch_up)		
		self.keyboard_event.add_connection(type = soya.sdlconst.KEYUP, \
			action = self.pitch_up)		
		self.keyboard_event.add_connection(type = soya.sdlconst.K_DOWN, \
			action = self.pitch_down)		
		self.keyboard_event.add_connection(type = soya.sdlconst.KEYDOWN, \
			action = self.pitch_down)
		self.keyboard_event.add_connection(type = soya.sdlconst.K_h, \
			action = self.help)
		self.keyboard_event.add_connection(type = soya.sdlconst.K_ESCAPE, \
			action = self.back)	
		self.keyboard_event.add_connection(type = soya.sdlconst.K_SPACE, \
			action = self.play_tone_wave)
		self.keyboard_event.add_connection(type = soya.sdlconst.K_l, \
			action = self.play_line_wave)
		self.keyboard_event.add_connection(type = soya.sdlconst.K_m, \
			action = self.play_tone_freq)
		self.keyboard_event.add_connection(type = soya.sdlconst.K_n, \
			action = self.play_line_freq)	
		self.keyboard_event.add_connection(type = soya.sdlconst.K_v, \
			action = self.play_tone_both)
		self.keyboard_event.add_connection(type = soya.sdlconst.K_b, \
			action = self.play_line_both)
		self.keyboard_event.add_connection(type = soya.sdlconst.K_d, \
			action = self.bpm_up)
		self.keyboard_event.add_connection(type = soya.sdlconst.K_c, \
			action = self.bpm_min)
		self.keyboard_event.add_connection(type = soya.sdlconst.K_u, \
			action = self.split_line)
		self.keyboard_event.add_connection(type = soya.sdlconst.K_i, \
			action = self.merge_lines)
		self.keyboard_event.add_connection(type = soya.sdlconst.K_a, \
			action = self.add_tone)
		self.keyboard_event.add_connection(type = soya.sdlconst.K_r, \
			action = self.rem_tone)
		self.keyboard_event.add_connection(type = soya.sdlconst.K_t, \
			action = self.change_text)





	
def main():
	pass

if __name__ == '__main__': main()

