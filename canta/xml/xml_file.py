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
import os


#import elementtree.ElementTree as ET
#import cElementTree as ET
#import lxml.etree as ET
import xml.etree.ElementTree as ET # Python 2.5


#from lib.theme.static_model import StaticModel
#from lib.theme.ani_model import AniModel
#from lib.theme.panel import Panel

class XmlFile:
	"""Parse a XML file for user config and/or theme elements.
	"""

	def __init__(self, xml_file, root_name, debug=0):
		self.root_name = root_name
		self.xml_file = xml_file
		self.debug = debug


	def read_config(self):
		try:
			self.tree = ET.parse(self.xml_file)
			root = self.tree.getroot()
			self.item = self.read_xml(root)
		except:
			self.write_xml()

	def read_xml(self, elem):
		if len(elem) > 0:
			target = {}
			for sub_elem in elem:
				child = self.read_xml(sub_elem)
				target[sub_elem.tag] = child
		else:
			target = elem.text

		return target

	def write_xml(self, ):
		# build a tree structure
		root = ET.Element(self.root_name)
		self.write_loop(root, self.item)

		# wrap it in an ElementTree instance, and save as XML
		tree = ET.ElementTree(root)
		tree.write(self.xml_file)

		'''with utf_8 encoding the parse-methode dont work or i dont know how'''
		#tree.write(self.xml_file, encoding='utf_8')


	def write_loop(self, elem, src_dict):
		
		for k,v in src_dict.iteritems():
			if type(v) == dict:
				child_elem = ET.SubElement(elem, k)
				self.write_loop(child_elem, v)
			else:
				child_elem = ET.SubElement(elem,k)
				child_elem.text = v
				 


