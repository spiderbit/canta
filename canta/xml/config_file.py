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


from xml_file import XmlFile



class ConfigFile(XmlFile):

	def __init__(self, xml_file, debug=0):
		XmlFile.__init__(self, xml_file, 'config', debug)
		self.item = {}
		self.item['sound'] = {}
		self.item['screen'] = {}
		self.item['theme'] = {}
		

		self.item['screen']['resolution'] = {}

		self.item['screen']['resolution']['x'] = '800'
		self.item['screen']['resolution']['y'] = '600'
		self.item['screen']['fullscreen'] = 'off'
		self.item['screen']['fps_label'] = 'off'
		self.item['screen']['pil'] = 'on'
		
		self.item['sound']['player'] = 'Gstreamer'
		self.item['sound']['input'] = 'Gstreamer'
		self.item['sound']['preview'] = 'on'

		self.item['theme']['name'] = 'default'
		self.item['misc'] = {}
		self.item['misc']['language'] = 'default'
		self.item['misc']['octave'] = 'off'


	# get theme properties


	def get_theme_name(self):
		return self.item['theme']['name']

	def get_fullscreen(self):
		return self.get_bool(self.item['screen']['fullscreen'])

	def get_res_x(self):
		return int(self.item['screen']['resolution']['x'])
		
	def get_res_y(self):
		return int(self.item['screen']['resolution']['y'])

	def get_player(self):
		return self.item['sound']['player']
		
	def get_input(self):
		return self.item['sound']['input']
		
	def get_preview(self):
		return self.get_bool(self.item['sound']['preview'])

	def get_fps_label(self):
		return self.get_bool(self.item['screen']['fps_label'])

	def get_pil(self):
		return self.get_bool(self.item['screen']['pil'])

	def get_locale(self):
		return self.item['misc']['language']

	def get_octave(self):
		return self.get_bool(self.item['misc']['octave'])


	# set theme properties

	def set_theme_name(self, new_val):
		self.item['theme']['name'] = new_val

	def set_fullscreen(self, new_val):
		self.item['screen']['fullscreen'] = new_val

	def set_res_x(self, new_val):
		self.item['screen']['resolution']['x'] = new_val
		
	def set_res_y(self, new_val):
		self.item['screen']['resolution']['y'] = new_val

	def set_player(self, new_val):
		self.item['sound']['player'] = new_val
		
	def set_input(self, new_val):
		self.item['sound']['input'] = new_val
		
	def set_preview(self, new_val):
		self.item['sound']['preview'] = new_val

	def set_fps_label(self, new_val):
		self.item['screen']['fps_label'] = new_val

	def set_pil(self, new_val):
		self.item['screen']['pil'] = new_val

	def set_locale(self, new_val):
		self.item['misc']['language'] = new_val

	def set_octave(self, new_val):
		self.item['misc']['octave'] = new_val

	# helpfull functions
	
	
	def get_bool(self, item):
		if item == "on":
			return 1
		elif item == "off":
			return 0
		else:
			print "BUG: Its not a bool on/off value!!!"
			sys.exit()



def main():

	config_file = ConfigFile('../../user_cfg.xml', debug=0)
	config_file.write_xml()

	print '\Config - config_items:', config_file.item
	


if __name__ == '__main__': main()
