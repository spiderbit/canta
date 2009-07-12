#! /usr/bin/python -O
# -*- coding: utf-8 -*-
#
#    CANTA - A free entertaining educational software for singing
#    Copyright (C) 2009  S. Huchler
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

#import time
import sys
import os
#import gettext
import user


from canta.menus.menu import Menu
from canta.menus.settings import Settings
from canta.menus.button import MenuButton
from canta.menus.item_group import MenuGroup
from canta.menus.browser import MenuBrowser
from canta.menus.text import MenuText
from canta.song.song_editor import SongEditor
from canta.display.sing_screen import SingScreen
from canta.song.song_manager import SongManager


from canta.display.language import LocaleManager

class MainMenu(Menu):
    def __init__(self, widget_properties, config, theme_mgr, camera, core=None):
        Menu.__init__(self, widget_properties)
        self.core = core
        self.config = config

        self.locale = self.config['misc']['locale']
        self.lm = LocaleManager(self.core.app_dir)
        valid_languages = self.lm.get_langs()
        self.lm.install(self.locale)


        self.theme_mgr = theme_mgr
        self.camera = camera
        # Button labels:
        l_start = _(u"Sing")#_(u'Party Mode')
        l_song_editor = _(u'Song Editor')
        l_about = _(u'About')
        l_quit2 = _(u'Quit')
        l_settings_main = _(u'Settings')
        l_back =  _(u'back')
        l_save =  _(u'save')
        l_save_quit =  _(u'save & restart')
        l_quit =  _(u'quit')

        # Menu headings:
        h1_main_menu =  _(u'Main Menu')
        h1_about =  _(u'About')
        h1_song_browser =  _(u'Choose a song...')


        # File paths:
        about_file = os.path.join('misc', 'ABOUT.txt')
        logo_path = 'logo.png'
        show_logo = False

        #self.menus['main'] = main_menu # obsolete?
        # About menu:
        about_menu = MenuText(self.widget_properties, top=self.screen_res_y / 3, \
                left=self.screen_res_x / 2)
        about_menu.set_heading(h1_about)
        about_back = MenuButton(l_back, widget_properties = self.widget_properties, \
            target = self)
        about_menu.add(about_back, 'horiz')
        about_quit = MenuButton(l_quit, function=self.quit, \
            pos_size=0, widget_properties = self.widget_properties)
        about_menu.add(about_quit, 'center')
        fd_license = open(os.path.join(self.core.app_dir, about_file), 'r')
        license = fd_license.read()
        about_menu.add_text(license)

        self.settings = Settings(self.config, self.widget_properties, self.lm, self, self.core)

        self.load_player()
        song_editor = SongEditor(self.core.app_dir, self.widget_properties, \
            self.theme_mgr, self, player=self.player)

        # Sing screen:
        sing_screen = SingScreen(app_dir=self.core.app_dir, main_menu=self, \
                    camera=self.camera, theme_mgr=self.theme_mgr, \
                    widget_properties=self.widget_properties, \
                    config=self.config, player=self.player)

        self.add_child(sing_screen)

        pos_size = {}
        pos_size['height'] = self.screen_res_y / 16
        pos_size['width'] = self.screen_res_x - 80
        pos_size['top'] = 10
        pos_size['left'] = 10

        # Song browser:
        entries = []
        entry_sing_screen = {}
        entry_sing_screen['song_start_text'] = 'Start'
        entry_sing_screen['start_screen'] = sing_screen
        entry_sing_screen['menu_text'] = _(u"Sing")
        entry_sing_screen['default_manager'] = 0
        entry_song_editor = {}
        entry_song_editor['song_start_text'] = 'Edit'
        entry_song_editor['start_screen'] = song_editor
        entry_song_editor['menu_text'] = _(u'Song Editor')
        entry_song_editor['default_manager'] = 1
        entries.append(entry_sing_screen)
        entries.append(entry_song_editor)

        browsers = []
        for entry in entries:
            browser = MenuBrowser(entry['default_manager'], self.widget_properties, \
                entry['start_screen'], self.config, player = self.player,\
                song_start_text=entry['song_start_text'])
            browser.set_heading(h1_song_browser)

            back_button = MenuButton(l_back, target=self, \
                widget_properties = self.widget_properties, \
                function=browser.stop_preview)
            quit_button = MenuButton(l_quit, function=self.quit, \
                pos_size=0, widget_properties = self.widget_properties)
            browser.add(back_button, 'center')
            browser.add(quit_button, 'center')
            browsers.append(browser)
            # Add buttons to main menu:
            args = {}
            args['selected'] = entry['start_screen']
            args['widgets'] = [self]
            self.add(MenuButton(entry['menu_text'], target=browser, function=browser.start_song,\
                widget_properties=self.widget_properties, pos_size=pos_size), 'center')

#        self.settings.init_menus(main_menu, pos_size)
        self.add(MenuButton(l_settings_main, target=self.settings, \
            widget_properties=self.widget_properties, pos_size=pos_size), 'center')
        self.add(MenuButton(l_about, target=about_menu, \
            widget_properties=self.widget_properties, pos_size=pos_size), 'center')
        self.add(MenuButton(l_quit2, function=self.quit, args=0, \
            widget_properties=self.widget_properties, pos_size=pos_size), 'center')


        use_pil = int(self.config['screen'].as_bool('pil'))
        # logo:
        if use_pil and show_logo:
            try:
                logo = pudding.control.Logo(self.parent, logo_path, z_index=4)
            except:
                pass

    def hide_loading_cont(self):
        # hide the loading label:
        self.loading_cont.visible = 0


    def show_loading_label(self):

        # Loading Label:
        # This should come immediatly, but it comes too late (after
        # the models are loaded).
        lc_top = self.config['screen'].as_int('resolution_x') / 2
        lc_left = self.config['screen'].as_int('resolution_x') / 2 - 100
        self.loading_cont = pudding.container.HorizontalContainer( \
                self.parent, \
                top=lc_top,
                left=lc_left,
                width=10, height=10, z_index=1)
        self.loading_cont.anchors = pudding.ANCHOR_RIGHT \
                     | pudding.ANCHOR_TOP | \
                    pudding.ANCHOR_LEFT
        self.loading_cont.add_child(pudding.control.SimpleLabel(
                    label=_(u'Loading, please wait...'),
                    font=self.widget_properties['font']['p']['obj'],
                    top=10,
                    left=10,
                    color=self.widget_properties['font']['p']['color']
                    ), pudding.EXPAND_HORIZ)



        if self.config['screen'].as_bool('fps_label'):
            pudding.ext.fpslabel.FPSLabel(soya.parent, \
                position = pudding.TOP_RIGHT)




    def quit(self, args=None):
        sys.exit(args)



    def load_player(self):
        sound_player = self.config['sound']['player']
        # The music players:
        if sound_player == 'Dummy':
            from canta.player.dummy_player import DummyPlayer
            self.player = DummyPlayer()
        elif sound_player == 'Gstreamer':
            from canta.player.gst_player import GSTPlayer
            self.player = GSTPlayer()
        else:
            print "something wrong in configfile, player not found!"
            sys.exit(0)

