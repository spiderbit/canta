#! /usr/bin/python -O
# -*- coding: utf-8 -*-
#
#    Pudding widget system Style class
#    Copyright (C) "Dunk" (dunk@dunkfordyce.co.uk)
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

import soya, os
from soya.opengl import *
import unittest

STYLE_NONE = -1

class Style:
    """Override the pudding default Style class to correct the system font error
        affecting some systems. Replicate the pudding style.py code and use our
        own font path. Also, use our own values for border fonts, widths
        and colors, since this is not (yet?) possible with pudding.
        This class is passed when we init pudding.
    """

    def __init__(self, widget_properties, debug=0):
        self.debug = debug

        self.default_font = widget_properties['font']['p']['obj']
        self.default_color = widget_properties['font']['p']['color']

        # Color used for slider only (?):
        self.box_background = widget_properties['box']['background']['color']
        self.box_border = widget_properties['box']['border']['color']
        self.box_border_width = widget_properties['box']['border']['width']

        self.button_border = widget_properties['button']['border']['off_focus']['color']
        # It's not possible to have seperate border_widths for on_focus and
        # off_focus.  Taking the on_focus value here:
        self.button_border_width = widget_properties['button']['border']['on_focus']['width']
        self.button_background = widget_properties['button']['background']['off_focus']['color']

        self.panel_font = self.default_font
        self.panel_font_color = self.default_color

        self.panel_bar = self.default_color

    def draw_bordered_box(self, width, height, background=None, border=None, border_width=None):
        glEnable(GL_BLEND)
        if background != STYLE_NONE:
            glColor4f( *( background or self.box_background))
            glBegin(GL_QUADS)
            glVertex3f( 0, 0, 0)
            glVertex3f( 0, height, 0)
            glVertex3f( width, height, 0)
            glVertex3f( width, 0, 0)
            glEnd()
            glColor4f( *( border or self.box_border) )
        if border != STYLE_NONE and border_width != 0:
            glLineWidth( border_width or self.box_border_width)
            glBegin(GL_LINE_STRIP)
            glVertex3f( 0, 0, 0)
            glVertex3f( 0, height, 0)
            glVertex3f( width, height, 0)
            glVertex3f( width, 0, 0)
            glVertex3f( 0, 0 , 0)
            glEnd()
        glDisable(GL_BLEND)

    def draw_button(self, width, height, background=None, border=None, border_width=None):
        self.draw_bordered_box(width, height, \
                    background or self.button_background, \
                    border or self.button_border, \
                    border_width or self.button_border_width)

    def draw_panel(self, width, height, background=None, border=None, border_width=None, label=''):
        self.draw_bordered_box(width, height, background, border, border_width)
        glPushMatrix()
        used_border_width = border_width or self.box_border_width
        glTranslatef(used_border_width, used_border_width, 0)
        self.draw_bordered_box(width - (2 * used_border_width), \
                    self.panel_font.height + 5, \
                    background = self.panel_bar, \
                    border_width = 0)
        if label:
            glColor4f(*self.panel_font_color)
            self.panel_font.draw(label, 2, 0, 0)
        glPopMatrix()


class TestStyle(unittest.TestCase):
    def testCreate(self):
        style = Style()

