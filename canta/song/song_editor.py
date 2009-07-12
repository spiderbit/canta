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

from canta.event.observers.lyrics_observer import LyricsObserver
from canta.event.observers.main_cube_observer import MainCubeObserver
from canta.event.observers.click_observer import ClickObserver
from canta.event.observers.music_notes import MusicNotes
from canta.event.subjects.song_data import SongData
from canta.song.song import Song
from canta.song.song import MingusSong
from canta.song.song import UltraStarFile
from canta.menus.menu import Menu
from canta.menus.button import MenuButton
from canta.menus.text import MenuText
from canta.menus.input_field import InputField
from canta.event.keyboard_event import KeyboardEvent
from canta.event.song_event import SongEvent
from canta.song.song_segment import SongSegment




class SongEditor(Menu):
    """TODO...
    """
    def __init__(self, app_dir, widget_properties, theme_mgr, main_menu, player):

        Menu.__init__(self, widget_properties)
        self.l_help_hint_0 = _(u'Press [h] for help...')
        self.l_help_hint_1 = _(u'Press [ESC] to go back...')
        self.l_help_hint = self.l_help_hint_0
        self.l_bpm = _(u'BPM: ')
        self.l_line_no = _(u'Line: ')
        self.separator = u' - '
        self.h_help = _(u'Help')
        self.help_file_path = os.path.join(app_dir, 'misc', 'HELP.txt')
        self.widget_properties = widget_properties
        self.app_dir = app_dir
        self.parent_widget = widget_properties['root_widget']
        self.theme_mgr = theme_mgr

        self.screen_res_x = int(widget_properties['config']['screen']['resolution'].split('x')[0])
        self.screen_res_y = int(widget_properties['config']['screen']['resolution'].split('x')[1])

        self.font_p = widget_properties['font']['p']['obj']
        self.color_p = widget_properties['font']['p']['color']

        self.font_h = widget_properties['font']['h1']['obj']
        self.color_h = widget_properties['font']['h1']['color']

        self.main_menu = main_menu
        self.help_hint_cont = pudding.container.VerticalContainer( \
                self, left=self.screen_res_x / 2.5, top=5)
        self.help_hint_cont.right = 10
        self.help_hint_cont.anchors = pudding.ANCHOR_ALL
        self.keyboard_event = KeyboardEvent(self.widget_properties, theme_mgr)

        self.txt_input = InputField(self.widget_properties, '')
        self.txt_input.label.visible = 0

        self.player = player
        self.__connect_keys__()
        self.msg = dict()


    def show(self, args):

        # get name of the selected song name from args:
        self.song = args[0]
        self.selected_song = self.song.info['mp3']
        self.song.writer = self.song.reader
        self.v_cont.visible = 1
        self.setup()


    def setup(self):
        # Sizes and positions for the lyrics:
        pos_size = {}
        pos_size['width'] = 70
        pos_size['height'] = 30
        pos_size['top'] = int(self.widget_properties['config']['screen']['resolution'].split('x')[1]) / 1.1 - 12
        pos_size['left'] = 35
        self.widget_properties['pos_size'] = pos_size
        self.widget_properties['anchoring'] = 'bottom'

        # We deactivate the "done"-color by giving it the same color as "to_sing":
        self.lyrics_to_sing_color = self.widget_properties['font']['lyrics']['to_sing']['color']
        self.widget_properties['font']['lyrics']['to_sing']['color'] = \
            self.widget_properties['font']['lyrics']['done']['color']

        # The observer for the lyrics:
        lyrics = LyricsObserver(self.widget_properties)

        # The observer for the symbolical musical representations:

        song_bar_color = {}
        song_bar_color['special'] = (1, 0, 0, 0.6)
        song_bar_color['freestyle'] = (0, 1., 0., 0.6)
        song_bar_color['normal'] = (0, 0., 1., 0.4)

        cube = MainCubeObserver(self.widget_properties['root_world'], \
                        song_bar_color)

        self.music_notes = MusicNotes(self.parent_world)

        self.pos = 0
        self.song_data = SongData()
        self.song_data.attach(lyrics)
        self.song_data.attach(cube)
        self.song_data.attach(self.music_notes)

        # The paths to the song:
        self.msg['song'] = self.song
        self.song.read()
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
        self.help_hint = pudding.control.SimpleLabel(self.help_hint_cont, \
                label=self.l_help_hint)

        self.add_child(self.help_menu)
        # needs testing
        #click_observer = ClickObserver(self.player)
        #self.song_data.attach(click_observer)

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
        self.help_menu.visible = 1
        self.help_hint.label = self.l_help_hint_1


    def quit_help(self):
        self.heading_label.visible = 1
        self.line_number_label.visible = 1
        self.bpm_number_label.visible = 1
        self.keyboard_event.reset()
        self.__connect_keys__()
        self.help_hint.label = self.l_help_hint_0
        self.help_menu.visible = 0
        self.refresh()


    def init_text_field(self):
        if self.edit_value == 'text':
            self.txt_input.label.value = self.song.lines[self.song.line_nr].segments[self.pos].text
        elif self.edit_value == 'bar':
            self.txt_input.label.value = self.song.info['bar_length']

        self.txt_input.label.visible = 1
        self.txt_input.post_method = self.end_change_text

    def change_text(self, obj):
        self.edit_value = obj
        self.init_text_field()
        self.parent_world.remove(self.keyboard_event)
        self.parent_world.add(self.txt_input)

    def end_change_text(self):
        if self.txt_input.done:
            if self.edit_value == 'text':
                self.song.lines[self.song.line_nr].segments[self.pos].text = self.txt_input.label.value
            elif self.edit_value == 'bar':
                self.song.info['bar_length'] = self.txt_input.label.value
        self.txt_input.label.visible = 0
        self.parent_world.remove(self.txt_input)
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
        if not end_tone:
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
        #   thread.exit()
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
        self.msg['song'] = self.song
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
        self.song.write()


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

    def make_line_pictures(self):
        self.make_line_picture(all=True)

    def make_line_picture(self, all=False):
        ming = MingusSong()
        ming.load_from_song(self.song)
        if all:
            ming.generate_pictures()
        else:
            ming.generate_picture(self.song.line_nr)
        self.refresh()

    def __connect_keys__(self):
        """Map soya keyboard events to methods."""
        # Maybe we better should move this in a
        # xml/config-file and parse it from there

        key = soya.sdlconst
        connections = []
        connections.append((key.K_q, self.back))
        connections.append((key.K_PAGEDOWN, self.prev))
        connections.append((key.K_PAGEUP, self.next))
        connections.append((key.K_LEFT, self.select_note, 'prev'))
        connections.append((key.K_RIGHT, self.select_note, 'next'))
        connections.append((key.K_PLUS, self.increase))
        connections.append((key.K_MINUS, self.minimize))
        connections.append((key.K_KP_PLUS, self.increase))
        connections.append((key.K_KP_MINUS, self.minimize))
        connections.append((key.K_s, self.save))
        connections.append((key.K_y, self.move_le))
        connections.append((key.K_x, self.move_ri))
        connections.append((key.K_UP, self.pitch_up))
        connections.append((key.KEYUP, self.pitch_up))
        connections.append((key.K_UP, self.pitch_up))
        connections.append((key.KEYUP, self.pitch_up))
        connections.append((key.K_DOWN, self.pitch_down))
        connections.append((key.KEYDOWN, self.pitch_down))
        connections.append((key.K_h, self.help))
        connections.append((key.K_ESCAPE, self.back))
        connections.append((key.K_SPACE, self.play_tone_wave))
        connections.append((key.K_l, self.play_line_wave))
        connections.append((key.K_m, self.play_tone_freq))
        connections.append((key.K_n, self.play_line_freq))
        connections.append((key.K_v, self.play_tone_both))
        connections.append((key.K_b, self.play_line_both))
        connections.append((key.K_d, self.bpm_up))
        connections.append((key.K_c, self.bpm_min))
        connections.append((key.K_u, self.split_line))
        connections.append((key.K_i, self.merge_lines))
        connections.append((key.K_a, self.add_tone))
        connections.append((key.K_r, self.rem_tone))
        connections.append((key.K_t, self.change_text, 'text'))
        connections.append((key.K_z, self.change_text, 'bar'))
        connections.append((key.K_g, self.make_line_pictures))
        connections.append((key.K_e, self.make_line_picture))

        for connection in connections:
            self.keyboard_event.add_connection(*connection)





def main():
    pass

if __name__ == '__main__': main()

# vim: ai ts=4 sts=4 et sw=4

