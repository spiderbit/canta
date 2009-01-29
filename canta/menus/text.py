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
import soya
import soya.pudding as pudding
from canta.menus.button import MenuButton
from canta.menus.menu import Menu

class MenuText(Menu):
    def __init__(self, widget_properties, top=0, left=0):
        Menu.__init__(self, widget_properties)

        self.widget_properties = widget_properties

        # heading and nav container inherited from Menu:
        self.widgets.append(self.heading_cont)
        self.widgets.append(self.nav_cont)

        # The container for the text:
        self.text_cont = pudding.container.VerticalContainer(
                self.parent_widget,
                top=top,
                left=left,
                z_index=1)
        self.text_cont.anchors = pudding.ANCHOR_ALL
        self.text_cont.padding = 15
        self.text_cont.visible = 0
        self.widgets.append(self.text_cont)


    def add(self, button, align='left'):
        self.nav_cont.add_child(button, pudding.EXPAND_BOTH)
        button.root=self

    def add_text(self, text):
        label = pudding.control.SimpleLabel(label=text, color=self.color_p)
        self.text_cont.add_child(label, pudding.CENTER_HORIZ)
        
