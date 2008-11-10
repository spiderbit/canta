#! /usr/bin/python -O
# -*- coding: utf-8 -*-
#
#    CANTA Song Creator Frontend
#    Copyright (C) 2008  S. Huchler
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

from canta.song.song import Song
from canta.song.song_segment import SongSegment
import canta.metadata as metadata

#from xdg import Mime
import getopt

import sys, os, string
import user, shutil
import wx
import os.path

def supported_formats():
	formats = []
	for ext, format in metadata.formats.iteritems():
		if format:
			formats.append(ext)
	return formats

how_to_get_help_msg = '''

Help to use this Programm:\tpython %s <-h|--help>

''' % (sys.argv[0])

unsupported_format_msg = '''
Format: not supported!
Supported formats are: 
%s
''' % ('\n'.join(supported_formats()))
# + how_to_get_help_msg

def get_error_msg(song_path):

	error_msg = """
ERROR:	A Directory with the Songname you picked is already there!!!

 	There are 3 possible reasons for this:

	1. Somebody else did this song before you and you downloaded
	   and saved it to your home-song directory.
		
	Solution: You dont need to make it again so you are Done!

	2. You did run this script before or made the song_directory
	   manually but used bad midi file and you will make it new.
	
	Solution: You have to delete the Song-directory:
			%s
		and then start this script again\n
	3. You mistacly called this script a second time but first time
		
	Solution: All is right just start canta and edit your song
		  with the Songeditor!
""" % (song_path)
	return error_msg

start_screen = """
-----------------------------------------------------------
------- -C-A-N-T-A-  _S_O_N_G_  |G|E|N|E|R|A|T|O|R| -------
-----------------------------------------------------------

	Press Enter if you like the preset in []
"""


usage = """
Usage:  %s [OPTION]... [FILE]

   -h, --help\t\t\tPrints this page
   -A, --ask\t\t\tcsg ask you all values
   -m, --midi-file=FILE\t\tmidi file (except all other opts)
   -t, --title=NAME\t\ttitle name (default=filename without extention)
   -a, --artist=NAME\t\tartist name (default=UNKNOWN) 
   -e, --entries=NUMBER\t\tentrys per line (default=5)
   -s, --spacing=LENGTH\t\tspacing between entries in line (default=8)
   -d, --duration=LENGTH\tduration of each entry (default=5)

LENGTH = <BEATS/SECONDS>
-d 5      <- means 5 beats
-d 5.5s   <- means 5.5 seconds

Examples:

GUI MODE:
# starts song_creator GUI version
\t> %s

MIDI Mode:
# generates a song with data from midi file

\t> %s example.ogg -m example.mid\t<allowed options: -tA>

QUICK MODE (without need of a midi):
# generates a song with the length of music file with sample lines

\t> %s example.ogg\t\t\t<allowed options: -tAaesd>

supported formats: <%s>
	
""" % (sys.argv[0], sys.argv[0], sys.argv[0], sys.argv[0], (', '.join(supported_formats())))



def print_error(error_msg):
	print	'\n\n\n'+error_msg+'\n\n\n'


def get_paths():
	'''
		returns:	(config_path, songs_path)
		config_path:	cantas config path
		songs_path:	path of the song path of the user
	'''
	config_path = os.path.join(user.home, '.canta')
	songs_path = os.path.join(config_path, 'songs')
	return (config_path, songs_path)


def create_path(song_name):

	config_path, songs_path = get_paths()
	song_path = os.path.join(songs_path, song_name)

	if not os.access(config_path, os.F_OK):
		os.mkdir(config_path)

	if not os.access(songs_path, os.F_OK):
		os.mkdir(songs_path)

	if not os.access(song_path, os.F_OK):
		os.mkdir(song_path)
	else:
		return -1
	return True


def check_file(file):
	'''
		 do check if file is readable and its no directory
	'''

	if not os.access(file, os.R_OK):
		print "Error:",file, "don't exist or not readable, check path and rights!"
		sys.exit(1)

	if os.path.isdir(file):
		print "Error:",file, "seems to be a path!"
		sys.exit(1)

			
def create_song(title, src_path, song_file, song_path, song):
	'''
		parameters: 
			title:		SongTitle
			artist:		ArtistName
			src_path:	path of src-file
			song_file:	name of the ogg file without path
			song_path:	target_path (path of the song in canta)
			mode:		midi and nomidi allowed if you want to use a midi for song-generation
			midi_file:	the midifile you want to use
	'''

	config_path, songs_path = get_paths()
	shutil.copy(os.path.join(src_path, song_file), song_path)	
	song.write_to_txt(os.path.join(song_path, title+'.txt'))


def create_song_object(song_path, song_file, midi_file = None):

	if midi_file != None:
		song.read_from_midi(midi_file)
		shutil.copy(midi_file, song_path)
	else:
		length = get_length(song_path, song_file)
		fill_song_object(song, length)


def get_length(audio_file_absolute):
	'''
		parameters: todo...
	'''
	f = metadata.get_format(audio_file_absolute)
	if f is None:
		return False # not a supported format
	return f.get_length()


def fill_song_object(song, length, entries_per_line = 5, tone_distance = 8, tone_duration = 5):

	bpm = 200
	song.info['bpm'] = bpm
	time_pos = 0
	beets = int(bpm * length / 60 * 4)
	line_length = entries_per_line * tone_distance
	for line in range(beets / line_length):
		line_start = line * line_length
		if line > 0:
			song.addSegment(SongSegment( "pause", line_start))
		for i in range(entries_per_line):
			song.addSegment(
				SongSegment(
					"note", line_start + (i * tone_distance),
					tone_duration, 12, "-"
					)
				)
		
	song.addSegment(SongSegment( "end", 0))


def get_song_path(song_name):
	config_path, songs_path = get_paths()
	return os.path.join(songs_path, song_name)


def get_long_song_name(artist, title):
	return artist + ' - ' + title


def get_song_name(song_file):
	parts = song_file.split('.')
	song_name=''

	if len(parts) <= 1:
		song_name = parts[0]
	else:
		for part in parts[:-1]:
			song_name += part + '.'
		song_name = song_name[:-1]
	song_name = string.upper(song_name[0]) + song_name[1:]
	return song_name


def do_ask(text, default=None):
	default_str = '[]'
	if default != None:
		default_str = '["' + str(default) + '"]'
	value = raw_input(text + ': ' + default_str + ' > ')
	if value == '':
		value = default
	return value


#############################################################################################################################





def cli_client(music_file_absolute, ask, midi_file, title, artist, entries, spacing, duration):

	print start_screen

	if ask:
		music_file = do_ask('Music file', music_file_absolute)
	if music_file_absolute != None:
		check_file(music_file_absolute)
	else:
		print "Error: You need a music file!!"
		sys.exit(1)
	
	if ask:
		midi_file = do_ask('Midi file', midi_file_absolute)
	if midi_file != None:
		check_file(midi_file)
	
	head, tail = os.path.split(music_file_absolute)
	music_file = tail
	src_path = head

	format = metadata.get_format(music_file_absolute)
	if not format:
		print unsupported_format_msg
		sys.exit()

	if title == None:
		title = get_song_name(music_file)
	if ask:
		title = do_ask('Song title', title)
	

	if artist == None:
		artist = 'UNKNOWN'
	if ask:
		artist = do_ask('Artist', artist)

	if not create_path(artist + ' - ' + title):
		msg = get_error_msg(song_path)
		print_error(msg)
		sys.exit(1)

	if midi_file == None and ask:
		entries = do_ask('Amount of entries per line', entries)
		spacing = do_ask('Space between entries[BEATS/SECONDS]', spacing)
		duration = do_ask('Duration of the entries[BEATS/SECONDS]', duration)

	spacing = get_time(spacing)
	duration = get_time(duration)
	entries = int(entries)
	

	song_path = get_song_path(get_long_song_name(artist, title))

	song = Song(  title=title, artist=artist, mp3 = music_file, debug = 0)

	if midi_file != None:
		song.read_from_midi(midi_file)
		shutil.copy(midi_file, song_path)
	else:
		length = format.get_length()
		if not length:
			print unsupported_format_msg
			sys.exit()
		fill_song_object(song, length, entries, spacing, duration)

	create_song(title, src_path, music_file, song_path, song)

	print "\n\tDone now start canta to edit the song\n"





#############################################################################################################################






class MainWindow(wx.Frame):
	def __init__(self, filename='file.txt'):
		super(MainWindow, self).__init__(None, size=(500,300), title='Canta Song Generator')

		self.SetAutoLayout(True)
		self.SetSizeHints(285,180,400,350)

		self.panel=wx.Panel(self,-1)

		lc=wx.LayoutConstraints()
		lc.right.SameAs(self,wx.Right)
		lc.left.SameAs(self,wx.Left)
		lc.top.SameAs(self,wx.Top)
		lc.bottom.SameAs(self,wx.Bottom)

		self.panel.SetConstraints(lc)
		
		self.panel.SetAutoLayout(True)

		self.filename = filename
		self.dirname = "."
		self.create_menu()


		self.file_lbl = wx.StaticText(self.panel, -1, "The Music File :",wx.Point(20,60))
		self.file_ctl = wx.TextCtrl(self.panel, 20, "", wx.Point(220, 60), wx.Size(140,-1))

		self.artist_lbl = wx.StaticText(self.panel, -1, "Artist Name :",wx.Point(20,90))
		self.artist_ctl = wx.TextCtrl(self.panel, 20, "", wx.Point(220, 90), wx.Size(140,-1))

		self.title_lbl = wx.StaticText(self.panel, -1, "Song Title :",wx.Point(20,120))
		self.title_ctl = wx.TextCtrl(self.panel, 20, "", wx.Point(220, 120), wx.Size(140,-1))


		self.button = wx.Button(self.panel, 10, "Generate Song", wx.Point(150, 200))


		wx.EVT_TEXT(self, 20, self.EvtText)
		wx.EVT_CHAR(self, self.EvtChar)
		wx.EVT_BUTTON(self, 10, self.OnClick)




	def create_menu(self):
		file_menu = wx.Menu()
		for id, label, help_text, handler in \
			[(wx.ID_OPEN, "&Open", "Open a file", self.on_open),\
				 (wx.ID_EXIT,"E&xit","Terminate the program", self.on_close)]:
			item = file_menu.Append(id, label, help_text)
			self.Bind(wx.EVT_MENU, handler, item)
      		#	filemenu.AppendSeparator()

		menuBar = wx.MenuBar()
		menuBar.Append(file_menu, "&File") # Add the file_menu to the MenuBar
		self.SetMenuBar(menuBar)  # Add the menuBar to the Frame


	def error_Msg(self, msg, title='Error'):
		error_md = wx.MessageDialog(self, msg, title, wx.OK|wx.ICON_ERROR)
		error_md.ShowModal()
		error_md.Destroy()
		return

	def OnClick(self, event):
		file_name_absolute = os.path.join(self.dirname, self.filename)
		check_file(file_name_absolute)

		title_error = "At least a Songtitle is needed for creating a Canta song"

		if self.title_ctl.GetValue() == '':
			self.error_Msg(title_error)
			return

		if self.artist_ctl.GetValue() == '':
			self.artist_ctl.SetValue('UNKNOWN')
			
		format = metadata.get_format(file_name_absolute)

		if not format:
			self.error_Msg(unsupported_format_msg)
			return

		song_name = get_long_song_name(self.artist_ctl.GetValue() ,self.title_ctl.GetValue())
		if not create_path(song_name):
			msg = get_error_msg(song_path)
			self.error_Msg(msg)
			return	
		song_path = get_song_path(song_name)

		song = Song(self.title_ctl.GetValue(), self.artist_ctl.GetValue(), self.filename, debug = 0)

		length = get_length(file_name_absolute)
		fill_song_object(song, length)

		create_song(song_name, self.dirname, self.filename, song_path, song)
		
	        dlg = wx.MessageDialog(self, 'Done, song created', 'Message', wx.OK|wx.ICON_INFORMATION)
        	dlg.ShowModal()
        	dlg.Destroy()

	def EvtText(self, event):
		pass

	def EvtChar(self, event):
		pass

	def on_close(self, event):
		sys.exit(0)

	def on_open(self, event):
		if self.ask_for_filename(style=wx.OPEN,
			**self.get_file_dialog_options()):
			self.file_ctl.SetValue(os.path.join(self.dirname, self.filename))
			self.title_ctl.SetValue(get_song_name(self.filename))

	# Helper methods:
	def get_file_dialog_options(self):
		''' Return a dictionary with file dialog options that can be
			used in both the save file dialog as well as in the open
			file dialog. '''
		wildcard = "Audio files (*.ogg, *.mp3 ...)|"
		for format in supported_formats():
			wildcard += '*.%s;' % (format)
		return dict(message="Choose a file", defaultDir=self.dirname,
			wildcard=wildcard)

	def ask_for_filename(self, **dialogOptions):
		dialog = wx.FileDialog(self, **dialogOptions)
		if dialog.ShowModal() == wx.ID_OK:
			user_provided_filename = True
			self.filename = dialog.GetFilename()
			self.dirname = dialog.GetDirectory()

		else:
			user_provided_filename = False
		dialog.Destroy()
		return user_provided_filename




####################################################################################################



def main():
			 
	try:
		opts, args = getopt.gnu_getopt(sys.argv[1:], "hAm:t:a:e:s:d:", \
						       ["help", "ask", "midi-file", "title=", "artist=", \
								"entries=", "spacing=", "duration="])

	except getopt.GetoptError, err:
		
		 # print help information and exit:
		 print str(err) # will print something like "option -a not recognized"
		 print usage
		 sys.exit(2)
    
	music_file = None
	midi_file = None
	title = None
	artist = None
	entries_per_line = "5"
	spacing = "8"
	duration = "5"
	ask = False
	#verbose = False

	if len(args) == 1:
		music_file = args[0]
		check_file(music_file)
	elif len(args) ==  0 and len(opts) == 0:
		app = wx.App()
		frame = MainWindow()
		frame.Show()
		app.MainLoop()
		sys.exit()
	elif len(args) == 0 and '--ask' or '-A' in argv:
		pass
	else:
		print sys.argv[0], 'requires a audio file '
		print usage
		sys.exit(2)
		

	for o, a in opts:
		if o in ('-m', '--midi-file'):
			midi_file = a
		elif o in ('-t', '--title'):
			title = a
		elif o in ('-a', '--artist'):
			artist = a
		elif o in ('-e', '--entries'):
			entries_per_line = int(a)
		elif o in ('-s', '--spacing'):
			spacing = a
		elif o in ('-d', '--duration'):
			duration = a
		#elif o == "-v":
			#verbose = True
		elif o in ("-A", "--ask"):
			ask = True
		elif o in ("-h", "--help"):
			print usage
			sys.exit(2)
		else:
			assert False, "unhandled option"

	cli_client(music_file, ask, midi_file, title, artist, \
			   entries_per_line, spacing, duration)				



def get_time(x):

	if len(x) == 0:
		return False
	try:
		tones = int(x)
		if tones > 0:
			return tones
		else:
			print usage
			sys.exit(2)
	except:
		if x[-1] == 's':
			try:
				time_sec = float(x[:-1])
				if time_sec > 0:
					tones = int(time_sec * 200 / 4)
					if tones == 0:
						tones = 1
					return tones
				else:
					print usage
					sys.exit(2)
			except:
				print usage
				sys.exit(2)

					



if __name__ == '__main__': main()

