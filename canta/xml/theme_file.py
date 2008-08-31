#! /usr/bin/python -O
# -*- coding: utf-8 -*-
#
#    CANTA - A free entertaining educational software for singing
#    Copyright (C) 2007, 2008  S. Huchler, A. Kattner, F. Lopez
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
from xml.dom import minidom, Node
from xml.etree import cElementTree as etree

class ThemeFile(XmlFile):

	def __init__(self, debug=0):
		XmlFile.__init__(self, 'theme', debug)
		self.theme_items = {}
		self.fonts = []

		self.box = {}
		self.box['border'] = {}
		self.box['background'] = {}

		self.button = {}
		self.button['border'] = {}
		self.button['background'] = {}

		self.bar = {}
		self.bar['songbar'] = {}

		self.models = []
		self.animodels = []
		self.panels = []
	

	def store_atmosphere(self, xml_node):
		"""Get XML element attributes for the <atmosphere> tag and append
			them to the theme dictionary.
		"""
		atmosphere = {}
		for node in xml_node.childNodes:
			if self.is_el_node(node):
				name = node.nodeName
				if name == 'clouds':
					atmosphere[str(name)] = self.get_attributes(node, 'name')
				else:
					atmosphere[str(name)] = self.get_attributes(node, 'color')

		self.theme_items['atmosphere'] = atmosphere


	def store_model(self, xml_node):
		model = {}
		model['name'] = xml_node.attributes.get('name').value
		for node in xml_node.childNodes:
			if self.is_el_node(node):
				name = node.nodeName
				if name == 'position' \
				or name == 'rotation' \
				or name == 'scale':
					model[str(name)] = self.get_attributes(node, 'coordinates')
				elif name == 'cellshading' \
				or name == 'shadow':
					model[str(name)] = self.get_attributes(node, 'bool')
				elif name == 'animation' \
				or name == 'envmap':
					model[str(name)] = self.get_attributes(node, 'string')
		self.models.append(model)


	def store_animodel(self, xml_node):
		model = {}
		model['name'] = xml_node.attributes.get('name').value
		for node in xml_node.childNodes:
			if self.is_el_node(node):
				name = node.nodeName
				if name == 'position' \
				or name == 'rotation' \
				or name == 'scale':
					model[str(name)] = self.get_attributes(node, 'coordinates')
				elif name == 'shadow':
					model[str(name)] = self.get_attributes(node, 'bool')
				elif name == 'action':
					model[str(name)] = self.get_attributes(node, 'name')
		self.animodels.append(model)


	def store_panel(self, xml_node):
		panel = {}
		panel['name'] = xml_node.attributes.get('name').value
		for node in xml_node.childNodes:
			if self.is_el_node(node):
				name = node.nodeName
				if name == 'position' \
				or name == 'rotation' \
				or name == 'scale':
					panel[str(name)] = self.get_attributes(node, 'coordinates')
				elif name == 'shadow':
					panel[str(name)] = self.get_attributes(node, 'bool')
				elif name == 'animation':
					panel[str(name)] = self.get_attributes(node, 'string')
				elif name == 'color':
					panel[str(name)] = self.get_attributes(node, 'color')
				elif name == 'texture':
					panel[str(name)] = self.get_attributes(node, 'name')
		self.panels.append(panel)


	def store_font(self, xml_node):
		"""Get XML element attributes for the <font> tag and append
			them to the theme dictionary.
		"""
		for node in xml_node.childNodes:
			if self.is_el_node(node):
				try:
					attr = node.attributes.get('type').value
				except:
					attr = 'None'
				font = {}
				font['element'] = str(node.nodeName)
				font['type'] = str(attr)
				font['attrs'] = self.get_font_attribs(node)
				self.fonts.append(font)
		self.theme_items['fonts'] = self.fonts


	def get_font_attribs(self, xml_node):
		attribs = {}
		for node in xml_node.childNodes:
			if self.is_el_node(node):
				name = node.nodeName
				if name == 'file':
					file_name = self.get_attributes(node, 'name')
					attribs['file_name'] = file_name
				elif name == 'color':
					color = self.get_attributes(node, 'color')
					attribs['color'] = color
		return attribs


	def store_button(self, xml_node):
		"""Get XML element attributes for the <font> tag and append
			them to the theme dictionary.
		"""
		for node in xml_node.childNodes:
			if self.is_el_node(node):
				name = node.nodeName
				type_ = node.attributes.get('type').value
				attrs = self.get_button_attribs(node)
				if name == 'background':
					self.button['background'][str(type_)] = attrs
				elif name == 'border':
					self.button['border'][str(type_)] = attrs
		self.theme_items['button'] = self.button


	def get_button_attribs(self, xml_node):
		attr = {}
		for node in xml_node.childNodes:
			if self.is_el_node(node):
				name = node.nodeName
				if name == 'color':
					color = self.get_attributes(node, 'color')
					attr['color'] = color

				elif name == 'width':
					width = self.get_attributes(node, 'int')
					attr['width'] = width
		return attr


	def store_box(self, xml_node):
		"""Get XML element attributes for the <box> tag and append
			them to the theme dictionary.
		"""
		for node in xml_node.childNodes:
			if self.is_el_node(node):
				name = node.nodeName
				if name == 'border':
					self.store_box_attribs(node, 'border')
				elif name == 'background':
					self.store_box_attribs(node, 'background')
		self.theme_items['box'] = self.box


	def store_box_attribs(self, xml_node, item_type):
		for node in xml_node.childNodes:
			if self.is_el_node(node):
				name = node.nodeName
				if name == 'color':
					attrs = self.get_attributes(node, 'color')
					if item_type == 'border':
						self.box['border']['color'] = attrs
					elif item_type == 'background':
						self.box['background']['color'] = attrs
				elif name == 'width':
					attrs = self.get_attributes(node, 'int')
					self.box['border']['width'] = attrs


	def store_bar(self, xml_node):
		for node in xml_node.childNodes:
			if self.is_el_node(node):
				try:
					type_ = node.attributes.get('type').value
				except:
					type_ = 'None'
				name = str(node.nodeName)
				attrs = self.get_bar_attribs(node)
				if name == 'songbar':
					self.bar['songbar'][str(type_)] = attrs
				else:
					self.bar[name] = attrs
		self.theme_items['bar'] = self.bar


	def get_bar_attribs(self, xml_node):
		attr = {}
		for node in xml_node.childNodes:
			if self.is_el_node(node):
				name = str(node.nodeName)
				attr[name] = self.get_attributes(node, name)
		return attr


	def store_theme(self, path):
		self.path = path
		if self.parse(path):
			self.store_theme_items()
			return True
		else:
			print '+ Canta + Warning: Theme NOT loaded!'
			return False


	def store_theme_items(self):
		for node in self.xml_root_node.childNodes:
			if self.is_el_node(node):
				name = node.nodeName
				if name == 'atmosphere':
					self.store_atmosphere(node)
				elif name == 'font':
					self.store_font(node)
				elif name == 'box':
					self.store_box(node)
				elif name == 'button':
					self.store_button(node)
				elif name == 'model':
					self.store_model(node)
				elif name == 'animodel':
					self.store_animodel(node)
				elif name == 'panel':
					self.store_panel(node)
				elif name == 'bars':
					self.store_bar(node)
		self.theme_items['models'] = self.models
		self.theme_items['animodels'] = self.animodels
		self.theme_items['panels'] = self.panels


	def parse(self, path):
		"""Let minidom parse the XML file.
		"""
		self.xml_file = path
		
		
	#try:
		self.tree = etree.parse(self.xml_file)
		root = self.tree.getroot()
		#for node in root:
		#	if node.tag = 
		print self.tree.findtext('sky_color')
		#print type(self.tree)#,len(self.tree)
	
		self.xml_doc = minidom.parse(path)
		self.xml_root_node = self.xml_doc.documentElement
		return True
	#except:
		return False


	def get_attributes(self, xml_node, item_type):
		"""Get attributes from XML elements.
		"""

		if item_type == 'bool':
			value = xml_node.attributes.get('value').value
			if value == 'on':
				return True
			else:
				return False

		if item_type == 'int':
			return int(xml_node.attributes.get('value').value)

		if item_type == 'float':
			return float(xml_node.attributes.get('value').value)

		if item_type == 'string':
			return xml_node.attributes.get('value').value

		if item_type == 'name':
			return xml_node.attributes.get('name').value

		if item_type == 'size':
			size = {}
			size['width'] = int(xml_node.attributes.get('width').value)
			size['height'] = int(xml_node.attributes.get('height').value)
			return size

		if item_type == 'font':
			font = {}
			font['name'] = xml_node.attributes.get('name').value
			font['width'] = int(xml_node.attributes.get('width').value)
			font['height'] = int(xml_node.attributes.get('height').value)
			return font

		if item_type == 'color':
			r = xml_node.attributes.get('r').value
			g = xml_node.attributes.get('g').value
			b = xml_node.attributes.get('b').value
			a = xml_node.attributes.get('a').value
			return (
					self.translate_color(r),
					self.translate_color(g),
					self.translate_color(b),
					self.translate_color(a)
					)
		if item_type == 'formula':
			r = float(xml_node.attributes.get('r').value)
			g = float(xml_node.attributes.get('g').value)
			b = float(xml_node.attributes.get('b').value)
			a = float(xml_node.attributes.get('a').value)
			return (r, g, b, a)
		if item_type == 'coordinates':
			x = float(xml_node.attributes.get('x').value)
			y = float(xml_node.attributes.get('y').value)
			z = float(xml_node.attributes.get('z').value)
			return (x, y, z)


	def is_el_node(self, xml_node):
		if xml_node.nodeType == Node.ELEMENT_NODE:
			return True
		else:
			return False

	def is_pr_node(self, xml_node):
		# seems to be a node with no subnodes and no parameters
		if xml_node.nodeType == Node.TREE_POSITION_PRECEDING:
			return True
		else:
			return False


	def translate_color(self, color):
		"""Translate a R,G,B,A color value from range 0 .. 255
			to range 0.0 .. 1.0.
			Range 0 .. 255 is common for imaging programs (e.g. The Gimp).
			Range 0.0 .. 1.0 is what the game engine expects.
		"""
		color_range = 256.0
		translated_color = 100.0 * float(color) / color_range
		return translated_color / 100.0


	def write_theme(self, path):
		pass


def main():

	xml_file = ThemeFile(debug=0)
	xml_file.store_theme('../../themes/default/theme_cfg.xml')

	print '\nMAIN:\nTheme - theme_items:', xml_file.theme_items
	print 'xml_file.fonts'
	for item in xml_file.fonts:
		print item
	
	print 'xml_file.box'
	print xml_file.box

	print 'xml_file.button'
	print xml_file.button

	print 'xml_file.bar'
	print xml_file.bar


if __name__ == '__main__': main()


