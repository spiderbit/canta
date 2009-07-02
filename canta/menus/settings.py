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


import sys
import os
#from canta.display.language import LocaleManager
from canta.menus.menu import Menu
from canta.menus.button import MenuButton
from canta.menus.item_group import MenuGroup
from canta.menus.browser import MenuBrowser
from canta.menus.text import MenuText
from canta.display.properties import DisplayProperties
from canta.theme.theme_manager import ThemeManager
import soya


class Settings(Menu):
    """Initialize
        * user configuration (screen resolution, fullscreen settings, selected theme, ...)
    """
    def __init__(self, config, widget_properties, locale_manager, main_menu, core=None):
        self.core = core
        self.main_menu = main_menu
        self.lm = locale_manager
        Menu.__init__(self, widget_properties)
        self.widget_properties = widget_properties
        self.config = config
        self.locale = self.config['misc']['locale']
        self.octave = int(self.config['misc'].as_bool('octave'))
        self.helper = int(self.config['misc'].as_bool('helper'))
        self.allowed_difference =  int(self.config['misc'].as_int('allowed_difference'))

        self.screen_res_x =  self.config['screen'].as_int('resolution_x')
        self.screen_res_y =  self.config['screen'].as_int('resolution_y')
        self.fullscreen_on = int(self.config['screen'].as_bool('fullscreen'))
        self.fps_label = int(self.config['screen'].as_bool('fps_label'))
        self.use_pil = int(self.config['screen'].as_bool('pil'))
        self.sound_player = self.config['sound']['player']
        self.sound_input = self.config['sound']['input']
        self.sound_preview = int(self.config['sound'].as_bool('preview'))
        self.theme_name = self.config['theme']['name']

#        self.app_dir = os.path.dirname(sys.argv[0])

 #       self.lm = LocaleManager(self.app_dir)
  #      self.lm.install(self.locale)

        self.disp = DisplayProperties()

        self.valid_sound_players = ['Dummy', 'Gstreamer']
        self.valid_sound_inputs = ['Gstreamer']

        pos_size = {}
        pos_size['height'] = self.screen_res_y / 16
        pos_size['width'] = self.screen_res_x - 80
        pos_size['top'] = 10
        pos_size['left'] = 10


        #def init_menus(self, main_menu, pos_size):
        # Button labels:
        l_settings_screen = _(u'Screen')
        l_settings_sound = _(u'Sound')
        l_settings_theme = _(u'Theme')
        l_settings_misc = _(u'Misc')
        l_back =  _(u'back')
        l_save =  _(u'save')
        l_save_quit =  _(u'save & restart')
        l_quit =  _(u'quit')

        # Menu headings:
        h1_settings_main =  _(u'Settings')
        h1_settings_screen =  _(u'Screen Settings')
        h2_settings_screen =  _(u'SCREEN:')
        h1_settings_sound =  _(u'Sound Settings')
        h2_settings_sound =  _(u'SOUND:')
        h1_settings_theme =  _(u'Theme Settings')
        h2_settings_theme =  _(u'THEME:')
        h1_settings_misc = _(u'Miscellaneous Settings')
        h2_settings_misc = _(u'Miscellaneous')

        # Settings:
        valid_languages = self.lm.get_langs()
        on_off_toggle = [_('off'), _('on')]
        i_resolution =  _(u'Resolution:')
        i_fullscreen =  _(u'Fullscreen:')
        i_fps_label =  _(u'FPS label:')
        i_pil =  _(u'Cover images:')
        i_sound_output =  _(u'Select sound output engine:')
        i_sound_input =  _(u'Select sound input engine:')
        i_song_preview =  _(u'Play preview in song browser:')
        i_theme =  _(u'Choose a theme:')
        i_lan = _(u'Choose a language:')
        i_octave = _(u'Octave correctness:')
        i_helper = _(u'Easier tone hitting:')
        i_allowed_difference = _(u'Allowed difference:')

       # Options parent menu:
        #self.options_menu_main = Menu(self.widget_properties)
        self.options_menu_main = self
        self.options_menu_main.set_heading(h1_settings_main)

        # Options sub menus:
        self.options_menu_screen = MenuGroup(self.widget_properties)
        self.options_menu_screen.set_heading(h1_settings_screen)
        self.options_menu_sound = MenuGroup(self.widget_properties)
        self.options_menu_sound.set_heading(h1_settings_sound)
        self.options_menu_theme = MenuGroup(self.widget_properties)
        self.options_menu_theme.set_heading(h1_settings_theme)
        self.options_menu_misc = MenuGroup(self.widget_properties)
        self.options_menu_misc.set_heading(h1_settings_misc)

        # Add buttons to options parent menu:
        self.options_menu_main.add(MenuButton(l_back, target=self.main_menu, \
            widget_properties=self.widget_properties, pos_size=pos_size), 'horiz')
        self.options_menu_main.add(MenuButton(l_save, function=self.save, \
            widget_properties = self.widget_properties, pos_size=pos_size), 'horiz')
        self.options_menu_main.add(MenuButton(l_save_quit, function=self.save, \
            args='quit', widget_properties=self.widget_properties, pos_size=pos_size), 'horiz')

        self.options_menu_main.add(MenuButton(l_settings_screen, target=self.options_menu_screen, \
            widget_properties=self.widget_properties, pos_size=pos_size), 'center')
        self.options_menu_main.add(MenuButton(l_settings_sound, target=self.options_menu_sound, \
            widget_properties=self.widget_properties, pos_size=pos_size), 'center')
        self.options_menu_main.add(MenuButton(l_settings_theme, target=self.options_menu_theme, \
            widget_properties=self.widget_properties, pos_size=pos_size), 'center')
        self.options_menu_main.add(MenuButton(l_settings_misc, target=self.options_menu_misc, \
            widget_properties=self.widget_properties, pos_size=pos_size), 'center')

        back_from_screen = MenuButton(l_back, target=self.options_menu_main, \
            widget_properties=self.widget_properties)
        back_from_sound = MenuButton(l_back, target=self.options_menu_main, \
            widget_properties=self.widget_properties)
        back_from_theme = MenuButton(l_back, target=self.options_menu_main, \
            widget_properties=self.widget_properties)
        back_from_misc = MenuButton(l_back, target=self.options_menu_main, \
            widget_properties=self.widget_properties)
        save_button = MenuButton(l_save, function=self.save, \
            widget_properties=self.widget_properties)
        save_quit_button = MenuButton(l_save_quit, function=self.save, \
            args='quit', widget_properties=self.widget_properties)

        # Add items to settings menus:
        self.options_menu_screen.add(back_from_screen, 'center')
        self.options_menu_screen.add(save_button, 'center')
        self.options_menu_screen.add(save_quit_button, 'center')

        self.options_menu_sound.add(back_from_sound, 'center')
        self.options_menu_sound.add(save_button, 'center')
        self.options_menu_sound.add(save_quit_button, 'center')

        self.options_menu_theme.add(back_from_theme, 'center')
        self.options_menu_theme.add(save_button, 'center')
        self.options_menu_theme.add(save_quit_button, 'center')

        self.options_menu_misc.add(back_from_misc, 'center')
        self.options_menu_misc.add(save_button, 'center')
        self.options_menu_misc.add(save_quit_button, 'center')



        res = str(self.screen_res_x) + 'x' + str(self.screen_res_y)
        if res in self.disp.valid_resolutions:
            selected_resolution = \
                self.disp.valid_resolutions.index(res)
        else:
            selected_resolution = 2

        screen_items = []
        screen_items.append({'info' : i_resolution,
                    'button_type' : 'toggle',
                    'toggle_items' : self.disp.valid_resolutions,
                    'selected_item' : selected_resolution})
        screen_items.append({'info' : i_fullscreen, 'button_type' : 'toggle', \
                    'toggle_items' : on_off_toggle,
                    'selected_item' : self.fullscreen_on})
        screen_items.append({'info' : i_fps_label, 'button_type' : 'toggle', \
                    'toggle_items' : on_off_toggle,
                    'selected_item' : self.fps_label})
        screen_items.append({'info' : i_pil, 'button_type' : 'toggle', \
                    'toggle_items' : on_off_toggle, \
                    'selected_item' : self.use_pil})
        screen_group = {'heading' : h2_settings_screen, 'items' : screen_items}
        self.options_menu_screen.add_group(screen_group)


        misc_items = []
        misc_items.append({'info' : i_lan,
                    'button_type' : 'toggle',
                    'toggle_items' : valid_languages,
                    'selected_item' : self.locale})
        misc_items.append({'info' : i_octave,
                    'button_type' : 'toggle',
                    'toggle_items' : on_off_toggle,
                    'selected_item' : self.octave})

        misc_items.append({'info' : i_helper,
                    'button_type' : 'toggle',
                    'toggle_items' : on_off_toggle,
                    'selected_item' : self.helper})
        misc_items.append({'info' : i_allowed_difference,
                    'button_type' : 'toggle',
                    'toggle_items' : ['1', '2', '3', '4', '5', '6', '7'],
                    'selected_item' : str(self.allowed_difference)})

        misc_group = {'heading' : h2_settings_misc, 'items' : misc_items}
        self.options_menu_misc.add_group(misc_group)


        if self.sound_player in self.valid_sound_players:
            self.selected_player = self.valid_sound_players.index(self.sound_player)
        else:
            self.selected_player = 1 # defaults to PyGame
        if self.sound_input in self.valid_sound_inputs:
            self.selected_input = self.valid_sound_inputs.index(self.sound_input)
        else:
            self.selected_input = 0 # defaults to OSS

        sound_items = []
        sound_items.append({'info' : i_sound_output,
                    'button_type' : 'toggle',
                    'toggle_items' : self.valid_sound_players,
                    'selected_item' : self.selected_player})

        sound_items.append({'info' : i_sound_input,
                    'button_type' : 'toggle',
                    'toggle_items' : self.valid_sound_inputs,
                    'selected_item' : self.selected_input})

        sound_items.append({'info' : i_song_preview,
                    'button_type' : 'toggle',
                    'toggle_items' : on_off_toggle,
                    'selected_item' : self.sound_preview})

        sound_group = {'heading' : h2_settings_sound, 'items' : sound_items}
        self.options_menu_sound.add_group(sound_group)
        theme_mgr = ThemeManager()
        available_themes = theme_mgr.get_theme_names(os.path.join(self.core.app_dir, 'media', 'themes'))

        if self.theme_name in available_themes:
            selected_theme = available_themes.index(self.theme_name)
        else: selected_theme = 0
        theme_items = []
        theme_items.append({'info' : i_theme,
                    'button_type' : 'toggle',
                    'toggle_items' : available_themes,
                    'selected_item' : selected_theme})
        theme_group = {'heading': h2_settings_theme, 'items' : theme_items}
        self.options_menu_theme.add_group(theme_group)




    def init_config_menu(self):

        top = self.box_cont.top

        self.group_cont = pudding.container.VerticalContainer( \
                self, top=top, left=30, width=100, z_index=1)
        self.group_cont.padding = 10
        self.heading_label = pudding.control.SimpleLabel( \
                self.group_cont, top=10, left=15, label=items['heading'], \
                font=self.font_p,
                color=self.color_h)

        bc_top = top + 25
        bc_left = 10
        bc_width = 10 # any number, we ANCHOR_ALL later
        bc_height = 10 # any number, we ANCHOR_ALL later

        box_cont = pudding.container.Container( \
                self, left=bc_left, top=bc_top, \
                width=bc_width, height=bc_height, z_index=-3)
        box_cont.right = 20
        box_cont.bottom = 30
        box_cont.anchors = pudding.ANCHOR_ALL
        box_cont.padding = 5

        box_left = 10
        box_width = self.screen_res_x - 40

        box_height = len(items['items']) * 65
        self.bg_box = pudding.control.Box(box_cont, \
                left=box_left, \
                width=box_width, \
                height=box_height, \
                background_color=self.box_bg_color, \
                border_color=self.box_border_color, \
                z_index=-3)
        self.bg_box.anchors = pudding.ANCHOR_TOP | pudding.ANCHOR_LEFT | pudding.ANCHOR_RIGHT


        for item in items['items']:
            self.info_label = pudding.control.SimpleLabel(self.group_cont, \
                label=item['info'], font=self.font_p, left=10, \
                color=self.color_p)
            if item['button_type'] == 'toggle':
                selected_item = item['selected_item']
                self.toggle_list.append(self.group_cont.add_child( \
                    MenuToggle(self.widget_properties, \
                    item['toggle_items'], selected_item)))
            elif item['button_type'] == 'button':
                self.group_cont.add_child(MenuButton(item['label'], \
                    item['function'], item['args'], \
                    self.widget_properties))
        self.group_count += 1


    def save(self, args=None):
        # Sucking values out of the pudding labels, wich is crap:
        toggle_map = [_('off'), _('on')]
        on_off_mapping = {toggle_map[0]: 'off', toggle_map[1]: 'on'}
        x, y = self.options_menu_screen.toggle_list[0].label.split('x')
        fs = on_off_mapping[self.options_menu_screen.toggle_list[1].label]
        fps = on_off_mapping[self.options_menu_screen.toggle_list[2].label]
        pil = on_off_mapping[self.options_menu_screen.toggle_list[3].label]

        sp = self.options_menu_sound.toggle_list[0].label
        si = self.options_menu_sound.toggle_list[1].label
        spr = on_off_mapping[self.options_menu_sound.toggle_list[2].label]

        tn = self.options_menu_theme.toggle_list[0].label

        locale = self.options_menu_misc.toggle_list[0].label
        octave = on_off_mapping[self.options_menu_misc.toggle_list[1].label]
        helper = on_off_mapping[self.options_menu_misc.toggle_list[2].label]
        allowed_difference = self.options_menu_misc.toggle_list[3].label


        self.config['screen'] = {
            'resolution_x' : x,
            'resolution_y' : y,
            'fullscreen' : fs,
            'fps_label' : fps,
            'pil' : pil
        }
        self.config['sound'] = {
            'player' : sp,
            'input' : si,
            'preview' : spr,
        }
        self.config['theme'] = {
            'name' : tn
        }
        self.config['misc'] = {
            'locale' : locale,
            'octave' : octave,
            'helper' : helper,
            'allowed_difference' : allowed_difference
        }
        self.config.write()

        if args == 'quit':
            soya.quit()
            self.core._start()  # starts recursive a new core needs better solution (reload)

