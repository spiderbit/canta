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

from xml.dom import minidom, Node
from canta.xml.theme_file import ThemeFile

import soya
import soya.cube
import soya.sphere

from canta.theme.static_model import StaticModel
from canta.theme.ani_model import AniModel
from canta.theme.panel import Panel

class Theme:
    """Create Soya objects from XmlFile objects.
    """
    def __init__(self, parent_world, theme_dir, theme_cfg_file, debug=0):
        self.debug = debug
        self.theme_dir = theme_dir
        self.parent_world = parent_world

        self.theme_file = ThemeFile(self.debug)
        path = os.path.join(self.theme_dir, theme_cfg_file)
        self.theme_file.store_theme(path)

        self.items = {}

        self.fonts = {}
        self.fonts['p'] = {}
        self.fonts['h1'] = {}
        self.fonts['lyrics'] = {}
        self.fonts['button'] = {}

        self.box = {}
        self.box['border'] = {}
        self.box['background'] = {}

        self.bar = self.theme_file.bar

        self.world = soya.World()

        self.create_fonts()
        self.box = self.theme_file.box
        self.button = self.theme_file.button

        self.create_atmosphere()
        self.create_models()
        self.create_animodels()
        self.create_panels()

        self.world.atmosphere = self.items['atmosphere']


    def create_fonts(self):
        height = soya.get_screen_height()

        # TODO: quick hack for font sizes, but it works for now.
        if height < 480:
        # 320x480
            p_w = 7 # paragraphs width, height
            p_h = 2
            h1_w = 9 # headings
            h1_h = 4
            ly_w = 7 # lyrics
            ly_h = 2
            bu_w = 7 # buttons
            bu_h = 2
        if height >= 480 and height < 600:
        # 640x480
            p_w = 11 # paragraphs width, height
            p_h = 6
            h1_w = 15 # headings
            h1_h = 10
            ly_w = 19 # lyrics
            ly_h = 14
            bu_w = 9 # buttons
            bu_h = 2
        elif height >= 600 and height < 720:
        # 800x600
            p_w = 15
            p_h = 10
            h1_w = 27
            h1_h = 17
            ly_w = 31
            ly_h = 23
            bu_w = 15
            bu_h = 10
        elif height >= 720 and height <= 768:
        # 1280x720
        # 1024x768
            p_w = 19
            p_h = 14
            h1_w = 31
            h1_h = 20
            ly_w = 43
            ly_h = 32
            bu_w = 17
            bu_h = 12
        elif height > 768 and height < 1024:
        # 1280x800
            p_w = 21
            p_h = 14
            h1_w = 39
            h1_h = 28
            ly_w = 45
            ly_h = 34
            bu_w = 25
            bu_h = 14
        elif height > 768 and height < 1050:
        # 1280x1024
            p_w = 25
            p_h = 16
            h1_w = 45
            h1_h = 34
            ly_w = 55
            ly_h = 45
            bu_w = 25
            bu_h = 16
        elif height >= 1050 and height < 1200:
        # 1400x1050
        # 1680x1050
            p_w = 31
            p_h = 24
            h1_w = 47
            h1_h = 36
            ly_w = 59
            ly_h = 56
            bu_w = 31
            bu_h = 21
        elif height >= 1200:
        # 1600x1200
        # 1920x1200
            p_w = 27
            p_h = 20
            h1_w = 56
            h1_h = 46
            ly_w = 75
            ly_h = 64
            bu_w = 31
            bu_h = 24
        else:
        # 800x600
            p_w = 15
            p_h = 10
            h1_w = 27
            h1_h = 17
            ly_w = 31
            ly_h = 23
            bu_w = 15
            bu_h = 10

        for font in self.theme_file.fonts:
            if font['element'] == 'p':
                self.fonts['p'][font['type']] = {}
                self.fonts['p'][font['type']]['color'] = font['attrs']['color']
                self.fonts['p'][font['type']]['font'] = soya.Font(
                        os.path.join(self.theme_dir, 'media', 'fonts',
                        font['attrs']['file_name']),
                        p_w,
                        p_h)
            elif font['element'] == 'h1':
                self.fonts['h1'][font['type']] = {}
                self.fonts['h1'][font['type']]['color'] = font['attrs']['color']
                self.fonts['h1'][font['type']]['font'] = soya.Font(
                        os.path.join(self.theme_dir, 'media', 'fonts',
                        font['attrs']['file_name']),
                        h1_w,
                        h1_h)
            elif font['element'] == 'lyrics':
                self.fonts['lyrics'][font['type']] = {}
                self.fonts['lyrics'][font['type']]['color'] = font['attrs']['color']
                self.fonts['lyrics'][font['type']]['font'] = soya.Font(
                        os.path.join(self.theme_dir, 'media', 'fonts',
                        font['attrs']['file_name']),
                        ly_w,
                        ly_h)
            elif font['element'] == 'button':
                self.fonts['button'][font['type']] = {}
                self.fonts['button'][font['type']]['color'] = font['attrs']['color']
                self.fonts['button'][font['type']]['font'] = soya.Font(
                        os.path.join(self.theme_dir, 'media', 'fonts',
                        font['attrs']['file_name']),
                        bu_w,
                        bu_h)



    def create_atmosphere(self):
        self.items['atmosphere'] = soya.SkyAtmosphere()
        self.items['atmosphere'].bg_color = self.theme_file.theme_items['atmosphere']['background_color']
        self.items['atmosphere'].sky_color = self.theme_file.theme_items['atmosphere']['sky_color']
        try:
            self.items['atmosphere'].cloud = soya.Material( \
                soya.Image.get(self.theme_file.theme_items['atmosphere']['clouds']))
        except:
            pass # does this work at all!?


    def create_models(self):
        for model in self.theme_file.theme_items['models']:
            if 'animation' in model:
                anim = model['animation']
            else:
                anim = None
            if 'envmap' in model:
                envmap = model['envmap']
            else:
                envmap = None
            StaticModel(self.world, model['name'], \
                model['position'],
                model['scale'],
                model['rotation'],
                model['shadow'],
                anim,
                model['cellshading'],
                envmap,
                self.debug)


    def create_animodels(self):
        for model in self.theme_file.theme_items['animodels']:
            AniModel(self.world, model['name'], \
                model['position'],
                model['scale'],
                model['rotation'],
                model['shadow'],
                model['action'],
                self.debug)


    def create_panels(self):
        
        panels = self.theme_file.theme_items['panels']
        for panel in panels:
            if 'color' in panel:
                color = panel['color']
            else:
                color = None
            if 'texture' in panel:
                texture = panel['texture']
            else:
                texture = None
            if 'shadow' in panel:
                shadow = panel['shadow']
            else:
                shadow = False
            if 'animation' in panel:
                anim = panel['animation']
            else:
                anim = None
            Panel(self.world, panel['name'], \
                panel['position'],
                panel['scale'],
                panel['rotation'],
                color,
                texture,
                anim,
                shadow,
                self.debug)


    def add_to_world(self):
        """Add theme to the scene.
        """
        self.parent_world.add(self.world)


    def remove_from_world(self):
        """Remove theme from the scene.
        """
        self.parent_world.remove(self.world)

def main():
    pass

if __name__ == '__main__': main()

