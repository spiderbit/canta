#! /usr/bin/python -O
# -*- coding: utf-8 -*-

# CANTA - A free entertaining educational software for singing
# Copyright (C) S. Huchler, A. Kattner, F. Lopez
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import soya.pudding as pudding
from canta.menus.button import MenuButton
from canta.menus.menu import Menu

class MidiEditor(Menu):
	"""TODO
	"""

	def __init__(self, app_dir, widget_properties, debug=0):
		Menu.__init__(self, widget_properties)
		self.debug = debug
		self.widget_properties = widget_properties
		self.app_dir = app_dir
		self.parent_widget = self.widget_properties['root_widget']

		self.box_border_color = widget_properties['box']['border']['color']
		self.box_bg_color = widget_properties['box']['background']['color']

		self.font_p = widget_properties['font']['p']['obj']
		self.color_p = widget_properties['font']['p']['color']
		self.font_h = widget_properties['font']['h1']['obj']
		self.color_h = widget_properties['font']['h1']['color']

		# A container for the global navigation:
		nc_top = 20
		nc_left = 20
		nc_height = self.widget_properties['screen']['height'] / 20
		self.nav_cont = pudding.container.HorizontalContainer( \
				self.parent_widget, left=nc_left, top=nc_top, \
				height=nc_height)
		self.nav_cont.right = 30
		self.nav_cont.anchors = pudding.ANCHOR_RIGHT \
					 | pudding.ANCHOR_TOP | \
					pudding.ANCHOR_LEFT
		self.nav_cont.padding = 5
		self.nav_cont.visible = 0

		# the container for all following items:
		self.channel_cont = pudding.container.VerticalContainer( \
					self.parent_widget, \
					left=10, top=210)
		self.channel_cont.padding = 5
		self.channel_cont.anchors = pudding.ANCHOR_ALL

		# a label for text:
		self.heading_label = pudding.control.SimpleLabel( \
					self.channel_cont, label='', font=self.font_h,
					color=self.color_h, top=0, left=35)

		self.channel_cont.visible = 0

		self.widgets = []
		self.widgets.append(self.nav_cont)
		self.widgets.append(self.channel_cont)


	def add(self, button, align = 'center'):
		self.nav_cont.add_child(button, pudding.EXPAND_BOTH)


	def show(self, args):
		for item in args[1]:
			item.visible = 0

		# get name of the selected song:
		selected_song = args[0]

		channelCount = 3
		
		# set label to selected filename:
		self.heading_label.label = selected_song

		# the channel box:
		for i in range(channelCount):
			_top = 20 + 105 * i
			self.label_channelText = 'Channel ' + str(i + 1)
			# a label for channel text:
			self.song_channel_text_label = pudding.control.SimpleLabel(
						self.channel_cont, top=_top, left=35, \
						label=self.label_channelText,
						font=self.font_p, color=self.color_p)

			# The select button:
			self.channel_cont.add_child(MenuButton( \
					'select', self.selectChannel, \
					None, self.widget_properties))

			self.ch_bg_box = pudding.control.Box(
						self.channel_cont, top=_top, \
						left=20, width=960, height=85, \
						background_color=self.box_bg_color,
						border_color=self.box_border_color)

			


		self.channel_cont.visible = 1
		self.nav_cont.visible = 1

		self.parent_widget.on_resize()

	def selectChannel(self,arg):
		print 'selectChannel(' + str(arg) + ')'

