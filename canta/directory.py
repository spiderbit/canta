#! /usr/bin/python -O
# -*- coding: utf-8 -*-
#
#    CANTA - A free entertaining educational software for singing
#    Copyright (C) 2007, 2008, 2009  S. Huchler, A. Kattner, F. Lopez
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

class Directory(object):
    def __init__(self, name):
        # only need unicode convertion here,
        # because i dont want break the api of
        # coreinit and songmenu(browser)name
        try:
            self.__name = unicode(name, 'utf-8', errors='replace')
        except:
            self.__name = name

    def make(self):
        if not os.path.exists(self.__name):
            os.mkdir(self.__name)
        elif os.path.isfile(self.__name):
            raise OSError('ERROR: a file with the same name as the desired ' \
                          'dir, "%s", already exists.' % self.__name)

    def change(self):
        os.chdir(self.__name)

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name


    name = property(get_name, set_name)

    def get_relative(self, start):
        '''returns the relative path to start'''
        return os.relpath(self.__name, start)

