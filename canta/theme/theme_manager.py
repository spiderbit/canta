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

import os
from canta.theme.theme import Theme

class ThemeManager:
    """TODO
    """
    def __init__(self, parent_world=None, debug=0):
        self.debug = debug
        self.parent_world = parent_world
        self.themes = {}
        self.theme_cfg_file = 'theme_cfg.xml'


    def get_theme(self, theme_name='', theme_dir=''):
        self.theme_name = theme_name

        self.themes[theme_name] = Theme(self.parent_world, theme_dir, self.theme_cfg_file, self.debug)

#	def get_all(self, themes_dir):
#		for dir_name in os.listdir(self.themes_path):
#			# search for hidden directories (e.g. .svn)
#			# and ignore them:
#			if dir_name[:1] != '.':
#				if dir_name in self.themes:
#					if self.debug: print 'Theme is already registered.'
#				else:
#					self.themes[dir_name] = \
#				Theme(self.parent_world, self.themes_path, \
#					dir_name, self.debug)


    def get_theme_names(self, themes_path):
        paths = []
        theme_names = []
        for path in os.listdir(themes_path):
            if not path.startswith('.'):
                paths.append(path)
        sorted = paths.sort()
        for name in paths:
            theme_names.append(name)		
        return theme_names


    def show_theme(self, theme_name):
        self.themes[theme_name].add_to_world()
        

    def hide_theme(self, theme_name):
        self.themes[theme_name].remove_from_world()


    def get_font(self, theme_name, element='p', type_='None', attr='color'):
        return self.themes[theme_name].fonts[element][type_][attr]


    def get_box(self, theme_name):
        return self.themes[theme_name].box

    def get_button(self, theme_name):
        return self.themes[theme_name].button

    def get_bar(self, theme_name):
        return self.themes[theme_name].bar
