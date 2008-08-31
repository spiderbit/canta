
import os
from canta.song.song import Song

class SongLoader:

	def __init__(self, debug = 0):
		#self.songs_path = songs_path
		self.debug = debug
		pass

	def unicode(self, list):
		new_list = []
		for elem in list:
			try:
				new_list.append(elem.decode('utf-8'))
			except UnicodeEncodeError:
				new_list.append(elem.decode('iso-8859-1'))
		return new_list


	def load_songs(self, songs_path):
		song_paths = []
		# create Song objects for every directory in the
		# songs directory and add them to the song list:

		# if you want to change stuff here:  http://docs.python.org/lib/os-file-dir.html
		songs = []
		covers = 0
		mp3s = 0
		for root, dirs, files in os.walk(songs_path):

			if ".svn" in dirs:
				dirs.remove(".svn")
			dirs.sort()
			for dir in dirs:
				absolute_path = os.path.join(songs_path,dir)
					
				for root, dirs, files in os.walk(absolute_path):
					
					for file in files:
						file = file.decode('utf-8')
						''' removed gif and bmp here (soya only supports jpeg and png)'''
						valid_picture_formats = ['jpg', 'jpeg', 'png']
						valid_sound_formats = ['ogg', 'mp3']
							
						lower_file = file.lower()
						if lower_file == "desc.txt":
							pass
						elif lower_file.endswith('.txt'):


							

							# The song:
							song = Song(debug=self.debug, path = root, file=file)
							song.read_from_us( type="headers")
							
							#print "Scanning Directory:\t<" + song.path + ">\n"
							files = self.unicode(files)
							self.search_songs(valid_picture_formats, song, files, 'cover')
							

							if 'cover' in song.info:
								#print "\t\tFOUND Cover <", song.info['cover'], ">"
								covers+=1


							self.search_songs(valid_sound_formats, song, files, 'mp3')

							if 'mp3' in song.info and song.info != None:
								mp3s+=1
								songs.append(song)
							
								
							
		#print mp3s, " Songs with ", covers, " valid Covers found!"
		return songs






	def search_songs(self, valid_formats, song, files, check_item):	# find/search files would be a better name?
		found = False
		files_with_right_format = []
		search = False
		'''file in txt file is right'''
		if check_item in song.info and song.info[check_item] != None and song.info[check_item] in files: 
			return #found = True
		elif check_item in song.info:	# k there there is at least some info for this item
			if song.info[check_item] != None: # k there is something i can search
				search = True
		for format in valid_formats:
			''' if something about that stands in the file
			when not searching only files with right extention '''
			if search:	
				item = self.remove_extention(song.info[check_item]) + "." + format
			
			for file in files:
				#print " ", item, file
				if search and item.lower() == file.lower():
					#print "exact file"
					found = True
					song.info[check_item] = file
					break
				# search for the right endings if thats the wrong file i cant detect it, 
				#but better sometimes  a wrong file instead of no file found
				elif file.lower().endswith(format):
					#print "found a file with right ending", file
					files_with_right_format.append(file)
				else:
					pass
				
			if found:
				break
		else:
			''' i take it if its more i think i better dont take it 
			because its to dangerous that its not the right file.'''
			if len(files_with_right_format) == 1: 
				'''print "FOUND 1 file with right ending but wrong name 
				i take what i get:<"+files_with_right_format[0]+">"'''
				song.info[check_item] = files_with_right_format[0]
				
			else:
				'''print "found some files with right ending for 
				"+ check_item + ": ", len (files_with_right_format)'''
				for file in files_with_right_format:
					''' bad hack but the covers have often a substring [CO] '''
					if (file.lower().find(check_item)) != -1 \
						    or (file.lower()).find("co") != -1: 
						#print "find cover or co in file", file.lower().find(check_item)
						song.info[check_item] = file
						break
#					else:
#						print file, ": ",file.lower().find(check_item), \
#						    (file.lower()).find("co")
				else:
					#print "\t\t\t<<<<<<<<<<<<<not Found>>>>>>>>>>>>>>>>>"
					if check_item in song.info:
						del song.info[check_item]





	def remove_extention(self, name):
		non_ext_file = (name.split('.'))[:-1]
		return '.'.join(non_ext_file)

