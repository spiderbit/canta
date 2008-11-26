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

import soya.pudding as pudding

class Menu:
	def __init__(self, widget_properties, debug=0):
		self.debug = debug

		self.widgets = []

		self.parent_widget = widget_properties['root_widget']
		self.parent_world = widget_properties['root_world']
		self.screen_res_x = widget_properties['config']['screen'].as_int('resolution_x')
		self.screen_res_y = widget_properties['config']['screen'].as_int('resolution_y')
		self.font_p = widget_properties['font']['p']['obj']
		self.color_p = widget_properties['font']['p']['color']
		self.font_h = widget_properties['font']['h1']['obj']
		self.color_h = widget_properties['font']['h1']['color']
		self.box_border_color = widget_properties['box']['border']['color']
		self.box_bg_color = widget_properties['box']['background']['color']
		self.hc_height = self.screen_res_y / 20

		vc_top = self.screen_res_y / 3
		vc_left = 40
		self.v_cont = pudding.container.VerticalContainer(
				widget_properties['root_widget'],
				left=vc_left,
				top=vc_top,
				z_index = 1)
		self.v_cont.anchors = pudding.ANCHOR_ALL
		self.v_cont.padding = 10
		self.v_cont.visible = 0
		self.widgets.append(self.v_cont)

		# The container for global navigation:
		nc_top = self.hc_height + 10
		nc_left = 20
		nc_height = self.screen_res_y / 20
		self.nav_cont = pudding.container.HorizontalContainer( \
				self.parent_widget, left=nc_left, top=nc_top, \
				height=nc_height)
		self.nav_cont.right = 30
		self.nav_cont.anchors = pudding.ANCHOR_RIGHT \
					 | pudding.ANCHOR_TOP | \
					pudding.ANCHOR_LEFT
		self.nav_cont.padding = 5
		self.nav_cont.visible = 0
		self.widgets.append(self.nav_cont)

		# The container for the background box:
		bc_top = nc_top + 10 + nc_height
		bc_left = 10
		bc_width = 10 # any number, we ANCHOR_ALL later
		bc_height = self.screen_res_y
		self.box_cont = pudding.container.Container( \
				self.parent_widget, left=bc_left, top=bc_top,\
				width=bc_width, height=bc_height)
		self.box_cont.right = 20
		self.box_cont.bottom = 30
		self.box_cont.anchors = pudding.ANCHOR_ALL
		self.box_cont.padding = 5
		self.box_cont.visible = 0

		box_left = 10
		box_width = self.screen_res_x - 40
		box_height = self.screen_res_y - bc_top - 25
		self.bg_box = pudding.control.Box(self.box_cont, \
				left=box_left, \
				width=box_width, \
				height=box_height, \
				background_color=self.box_bg_color, \
				border_color=self.box_border_color, \
				z_index=-3)
		self.bg_box.anchors = pudding.ANCHOR_ALL

		# The container for the heading:
		self.heading_cont = pudding.container.HorizontalContainer( \
			self.parent_widget, left=20, top=10, \
			height=self.hc_height)
		self.heading_cont.right = 15
		self.heading_cont.anchors =  pudding.ANCHOR_RIGHT \
				 | pudding.ANCHOR_TOP | pudding.ANCHOR_LEFT
		self.heading_cont.padding = 5
		self.heading_cont.visible = 0
		self.widgets.append(self.heading_cont)


	def add(self, button, cont_type='vert'):
		if cont_type == 'horiz':
			self.nav_cont.add_child(button, pudding.EXPAND_BOTH)
		else:
			self.v_cont.add_child(button, pudding.CENTER_VERT)
		button.root=self
			

	def show(self):
		for item in self.widgets:
			item.visible=1
			if type(item) == pudding.container.VerticalContainer \
				or type(item) == pudding.container.HorizontalContainer \
					or type(item) == pudding.core.Container:
				for child in item.children:
					child.visible = 1
	
				
	def hide(self):
		for item in self.widgets:
			item.visible=0
			if type(item) == pudding.container.VerticalContainer \
				or type(item) == pudding.container.HorizontalContainer \
					or type(item) == pudding.core.Container:
				for child in item.children:
					child.visible = 0
		
		

	def set_heading(self, text):
			self.heading_cont.add_child(pudding.control.SimpleLabel( \
				label=text, font=self.font_h, \
				color=self.color_h), pudding.EXPAND_BOTH)

	def set_bg_box(self):
		self.widgets.append(self.box_cont)

