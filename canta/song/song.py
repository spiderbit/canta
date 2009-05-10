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

    def __init__(self, title='', artist='', mp3 = None, path='', bpm=0, gap=0, \
            start=0, line_nr=0, octave=False, reader=None, writer=None, debug=0):
        self.path = unicode(path, 'utf-8', errors='replace')		# only need this because i dont want break the api of coreinit and songmenu(browser)
        self.splitted = False
        self.debug = debug
        self.info = {}
        self.info['title'] = title
        self.info['artist'] = artist
        self.info['mp3'] = mp3
        self.info['bpm'] = bpm
        self.info['gap'] = gap
        self.info['start'] = start
        self.info['bar_length'] = '16'
        self.line_nr = line_nr
        self.pos = None
        self.end = False
        self.segments = []
        self.lines = []
        self.octave = octave
        self.reader = reader
        self.writer = writer


    def __cmp__(self, other):
        """Returns True if other and self have identical attributes"""

        if self.__dict__ == other.__dict__:
            return True
        else:
            return False



    def read(self, reader=None, mode='segments'):
        if reader:
            self.reader = reader
        self.reader.read(self, mode)


    def write(self, writer=None):
        if writer:
            self.writer = writer
        self.writer.write(self)


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

    def get_pitch_between(self, start_time, end_time):
        line_nr, tone_nr = self.get_pos(end_time)
        if not tone_nr:
            line_nr, tone_nr = self.get_pos(start_time)
        if tone_nr != None:# and len(self.song.lines[self.song.line_nr].segments) < self.song.pos:
            target_pitch = self.lines[line_nr].segments[tone_nr].pitch
        else:
            target_pitch = None
        return target_pitch


    def get_midi(self, line_nr, tone_nr):
        midi_tone = self.lines[line_nr].segments[tone_nr].pitch + 60 #72
        return midi_tone


    def get_freq(self, line_nr, tone_nr):

        midi_tone = self.get_midi(line_nr, tone_nr)
        freq = 440 * 2**(float(midi_tone-69)/12.)
        return freq


from mingus.containers import Bar, Note, Track, Composition
import mingus.extra.LilyPond as LilyPond


li_header = """
\paper{
  %annotate-spacing = ##t
  paper-width = 15\cm
  left-margin = 0\cm
  right-margin = 0\cm
  top-margin = 0\cm
  %ragged-last-bottom = ##t
  %between-system-space = 0\cm
  %between-system-padding = 0\cm
  indent = #0
  head-separation = 2\mm
  %page-spacing-weight = 0
  %between-title-space = 0
  %before-title-space = 0
  %ragged-right=##t
  page-top-space = 0\cm
  force-assignment = #""
  line-width = #(- line-width (* mm  0.000000))
}
"""




class MingusSong:

    def __init__(self):
        self.composition = Composition()
        self.path = ''
        self.song_name = ''
        self.bar_length = 16

    def load_from_song(self, song):
        ''' Fills a mingus-composition object with the data of a Song object '''

        if 'bar_length' in song.info:
            try:
                self.bar_length = song.info['bar_length']
            except:
                print "You need to specify length of a Bar first before you can do this"
        for line in song.lines:
            track = Track()
            bar = Bar()
            for segment in line.segments:
                if segment.type == 'pause':
                    int_val = None
                elif segment.type == 'note':
                    int_val = segment.pitch
                n = Note().from_int(int_val + 48)
                note_length = float(self.bar_length) / segment.duration
                if not bar.place_notes(n, note_length):
                    track.add_bar(bar)
                    bar = Bar()
                    bar.place_notes(n, note_length)
            track.add_bar(bar)
            self.composition.add_track(track)
        self.path = song.path
        self.song_name = song.reader.file_name[:-4]


    def generate_pictures(self):
        ''' Generates pictures of the lines of notes '''
        for k, track in enumerate(self.composition.tracks):
            self.generate_picture(k)


    def generate_picture(self, k):
        ''' Generates picture of the lines k '''
        img_path = os.path.join(self.path, 'media', 'images')
        if not os.path.exists(img_path):
            os.makedirs(img_path)
        import tempfile
        tmp_dir = tempfile.mkdtemp()
        track = self.composition.tracks[k]
        ltrack = LilyPond.from_Track(track)
        tmp_file = os.path.join(tmp_dir, 'tmp_file')
        lily_str = li_header + ltrack
        LilyPond.save_string_and_execute_LilyPond(lily_str, tmp_file, '-fps')
        img_file = os.path.join(img_path, self.song_name + str(k) + '.png')
        gs_cmd = 'gs -dBATCH -dNOPAUSE -g2048x256 -q -r273.5 ' \
                +'-sDEVICE=pngalpha -sOutputFile="%s" "%s"' \
                % (img_file, tmp_file + '.ps')
        from subprocess import Popen
        p = Popen(gs_cmd, shell=True)
        sts = os.waitpid(p.pid, 0)
        os.unlink(tmp_file + '.ps')
        os.rmdir(tmp_dir)


class MidiFile_:

    def __init__(self, path=None, file_name=None):
        self.path = path
        self.file_name = file_name


    def read(self, song, mode='full'):
        """Parse a midi file and fill with that data the SongSegment list.

        Keyword arguments:
        midi_file -- the midi file to parse

        """

        file_name = os.path.join(self.path, self.file_name)
        f = open(file_name, 'rb')

        # do parsing
        x = MidiToText(song)
        midiIn = MidiInFile(x, f)
        midiIn.read()
        f.close()

    '''
    TODO: replace our old midi code with this
          when mingus midi-code gives correct position data
          probaply with version 0.5 see bugtracker

    def read(self, song, mode='full'):
        """Parse a midi file and fill with that data the SongSegment list.

        Keyword arguments:
        midi_file -- the midi file to parse

        """

        file_name = os.path.join(self.path, self.file_name)

        # do parsing
        from mingus.midi import MidiFileIn
        composition, bpm = MidiFileIn.MIDI_to_Composition(file_name)
        print bpm
        if len(composition.tracks) == 1:
            track = composition.tracks[0]
        #print track
        for bar in track.bars:
            line = SongLine()
            print "length:", bar.meter
            for note_cont in bar:
                if len(note_cont[2]) > 0:
                    note = note_cont[2][0]      # normaly a notecontainer should only have 1 note
                    print note_cont, int(note)-48  # us-values are 4 octaves lower than midi
                    print note.dynamics
                else:
                    print note_cont
#                SongSegment('note', time_stamp, duration=0, pitch=0, text="", special=False, freestyle=False):
              #  line.segments.append(
        import sys
        sys.exit(0)

    '''


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
            midi.update_time(96	 * (line.segments[i+1].time_stamp \
                            - segment.time_stamp - segment.duration))

        midi.note_on(ch, line.segments[-1].pitch+60, 0x64)
        midi.update_time(96 * line.segments[-1].duration)
        midi.note_off(ch, line.segments[-1].pitch+60, 0x40)
        midi.update_time(0)
        midi.end_of_track()
        midi.eof() # currently optional, should it do the write instead of write??
        midi.write()



class UltraStarFile:

    def __init__(self, path=None, file_name=None):
        self.file_name = file_name
        self.path = path



    def __cmp__(self, other):
        """Returns True if other and self have identical attributes"""

        if self.__dict__ == other.__dict__:
            return True
        else:
            return False

    def read(self, song, mode='segments'):
        """Parse a ultrastar-txt file and add header and segments to this object.

        Keyword arguments:
        file_name -- the Ultrastar file to parse
        mode -- 'segments' | 'headers' | 'full' full is headers + segments  (default 'segments')

        """

        us_file = os.path.join(self.path, self.file_name)
        f = open(us_file, 'r')
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

            if (mode == "headers" or mode == "full") and line.startswith('#'):
                words = line.strip('#').split(':')
                if len(words) == 2:
                    if words[0] == 'BPM' \
                        or words[0] == 'GAP' \
                        or words[0] == 'START':

                        song.info[words[0].lower()] \
                            = float(words[1].strip().replace(',', '.'))
                    elif words[0] == 'MP3':
                        song.info[words[0].lower()] \
                            = words[1].strip()
                    else:
                        song.info[words[0].lower()] \
                            = words[1].strip()
                else:
                    print 'error: something wrong in the songfile:'\
                        + us_file, words
            elif mode=="headers":
                # that must accellerate header-parsing for song-browser on startup
                return

            elif mode=="full" or mode == "segments":
                self.parse_segment(song, line)
        song.convert_to_absolute()


    def parse_segment(self, song, line):
        if line.startswith('-'):
            words = line.split(' ')
            if len(words) == 1:
                song.addSegment(SongSegment( "pause", \
                    float(words[0][1:]), '', '', ''))
            elif len(words) == 2:
                song.addSegment(SongSegment( "pause", \
                    float(words[1]), '', '', ''))
            elif len(words) == 3:
                song.addSegment(SongSegment( "pause", \
                    float(words[2]), '', '', ''))
            else:
                print 'Song - readFile()-error: something wrong in the songfile'
                sys.exit()

        # Find out if the note is a
        #   : <- normal note
        #   * <- special note
        #   F <- freestyle note
        elif line.startswith(':') or line.startswith('*') or line.startswith('F'):
            words = line.split(' ', 4)
            special = freestyle = False
            if line.startswith('*'):
                special = True
            elif line.startswith('F'):
                freestype = True
            time_stamp = int(words[1])
            duration = int(words[2])
            pitch = int(words[3])
            if not song.octave:
                pitch = pitch
            if len(words) == 5:
                text = words[4]
            else:
                text = ""

            song.addSegment(SongSegment("note", \
                        time_stamp, \
                        duration, \
                        pitch, \
                        text, special, freestyle))

        elif line.startswith('E'):
            song.addSegment(SongSegment("end", \
                float(song.segments[-1].time_stamp), '', '', ''))






    def write(self, song):
        file_name = os.path.join(self.path, self.file_name)
        songFile = codecs.open(file_name, encoding='utf-8', mode='w+')

        for key,value in song.info.iteritems():
            songFile.write(
                u'#' + \
                    key.upper() + u':' \
                    + unicode(value) + u'\n'
                )



        for segment in song.segments:

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







def main(): # main

    class_name = "Song"
    print "TESTCODE FOR CLASS: [%s]" % (class_name)

    song = Song(title='Test title', artist='artist', mp3='test.mp3')

    song.addSegment(SongSegment( "note", 19, 5, 12, "hallo"))
    song.addSegment(SongSegment( "note", 24, 5, 33, "blub"))
    song.addSegment(SongSegment( "note", 29, 2, 69, "was"))
    song.addSegment(SongSegment( "note", 31, 5, 17, "geh-ht"))
    song.addSegment(SongSegment( "note", 39))
    song.addSegment(SongSegment( "note", 42, 5, 12, "es"))
    song.addSegment(SongSegment( "note", 47, 5, 6, "geht"))
    song.addSegment(SongSegment( "note", 52, 2, 2, "fast"))
    song.addSegment(SongSegment( "note", 54, 5, 3, "alles"))

    print
    for k,v in song.info.iteritems():
        print "%s:\t\t %s" % (k,v)

    print "\n\nType\tTimeStamp\tDuration\tPitch\t\tText"

    for segment in song.segments:

        print "%s\t%s\t\t%s\t\t%s\t\t%s" % (segment.type, segment.time_stamp,
            segment.duration, segment.pitch, segment.text)
    song_file = 'Song.txt'
    print
    song.write_to_txt(song_file)
    print "wrote file %s" % (song_file)
    print

if __name__ == '__main__': main()

