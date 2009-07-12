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


# good example:  http://www.learningpython.com/2006/12/03/translating-your-pythonpygtk-application/

import os
import sys
import locale
import gettext

class LocaleManager:

    def __init__(self, app_dir = os.path.dirname(sys.argv[0])):
        self.app_dir = app_dir
        self.locale_path = os.path.join( self.app_dir, 'locale')
        self.langs = []

    def get_langs(self):
        self.load_langs()
        self.langs.insert(0,'default')
        return self.langs


    def install(self, lang):
        #1. way
        # application can set the wished language:
        if lang == 'System Setting':
            self.install_default()
        else:
            lang = gettext.translation( 'canta', self.locale_path, languages=[lang])
            lang.install(unicode=1)


    def install_default(self):
        # if you choose this way gettext looks what language ist set in env
        # you can choose that with: export LANG=de_DE
        gettext.install('canta', self.locale_path, unicode=1)

    def load_langs(self):

        #Get the local directory since we are not installing anything
        locale = os.listdir(self.locale_path)
        for lang in locale:
            self.langs.append(lang[0:2])

