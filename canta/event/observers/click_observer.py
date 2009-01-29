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


import os,sys


class ClickObserver:
    def __init__(self, player):
        self.player = player
        self.player.init_click()


    def click(self):
        # needs to be implemented
        self.player.click()


    def _next_line(self, song):	
        pass
        #sound

    def update(self, subject):
        status = subject.data['type']
        if status == 'roundStart':
            pass
        elif status == 'activateNote':
            self.click()
        elif status == 'deActivateNote':
            self.click()
        elif status == 'nextLine':
            pass
        elif status == 'end':
            pass
        elif self.debug:
            print 'status: ', status

