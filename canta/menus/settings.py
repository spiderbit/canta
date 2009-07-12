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
from canta.menus.menu import Menu
from canta.menus.button import MenuButton
from canta.menus.item_group import MenuGroup
from canta.menus.browser import MenuBrowser
from canta.menus.text import MenuText
from canta.display.properties import DisplayProperties
from canta.theme.theme_manager import ThemeManager
import soya

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)


class Settings(Menu):
    """Initialize
        * user configuration (screen resolution, fullscreen settings, selected theme, ...)
    """
    def __init__(self, config, widget_properties, locale_manager, main_menu, core=None):
        Menu.__init__(self, widget_properties)
        self.core = core
        self.main_menu = main_menu
        self.widget_properties = widget_properties
        self.config = config
        self.disp = DisplayProperties()

        pos_size = {}
        pos_size['height'] = self.screen_res_y / 16
        pos_size['width'] = self.screen_res_x - 80
        pos_size['top'] = 10
        pos_size['left'] = 10

        # Button labels:
        l_back =  _(u'back')
        l_save =  _(u'save')
        l_save_quit =  _(u'save & restart')
        l_quit =  _(u'quit')

        # Menu headings:
        h1_settings_main =  _(u'Settings')

        # Settings:
        on_off_toggle = [('off'), ('on')]

       # Options parent menu:
        self.options_menu_main = self
        self.options_menu_main.set_heading(h1_settings_main)

        # Add buttons to options parent menu:
        self.options_menu_main.add(MenuButton(l_back, target=self.main_menu, \
            widget_properties=self.widget_properties, pos_size=pos_size), 'horiz')
        #self.options_menu_main.add(MenuButton(l_save, function=self.save, \
        #    widget_properties = self.widget_properties, pos_size=pos_size), 'horiz')
        #self.options_menu_main.add(MenuButton(l_save_quit, function=self.save, \
        #    args='quit', widget_properties=self.widget_properties, pos_size=pos_size), 'horiz')

        # Options sub menus:
        for k, v in self.config.iteritems():
            # Options sub menus:
            menu = MenuGroup(self.widget_properties, key=k)
            menu.set_heading(_(k[0].upper() + k[1:]) + ' ' + _('Settings'))

            self.options_menu_main.add(
                MenuButton(_(k[0].upper() + k[1:]), target=menu, \
                widget_properties=self.widget_properties, \
                pos_size=pos_size), 'center')
            back_from_screen = MenuButton(l_back, \
                target=self.options_menu_main, \
                widget_properties=self.widget_properties)

            save_button = MenuButton(l_save, function=self.save, \
                args=[menu, 'go_on'], widget_properties=self.widget_properties)
            save_quit_button = MenuButton(l_save_quit, function=self.save, \
                args=[menu, 'quit'], widget_properties=self.widget_properties)

            # Add items to settings menus:
            menu.add(back_from_screen, 'center')
            menu.add(save_button, 'center')
            menu.add(save_quit_button, 'center')

            x_items = []
            for key, value in v.iteritems():
                item_spec = v.configspec[key]
                if item_spec.startswith('boolean'):
                    if value == True:
                        toggle='on'
                    else:
                        toggle='off'
                    x_items.append({'info' : _(key),
                        'button_type' : 'toggle',
                        'toggle_items' : on_off_toggle,
                        'selected_item' : toggle})
                elif item_spec.startswith('option'):
                    options = item_spec.strip('option(').strip(')').split(',')
                    choices = []
                    for option in options:
                        option = option.strip().replace("'", '')
                        if option.startswith('default='):
                            default_value = option.split('=')[1]
                        else:
                            choices.append(option.strip())
                    try:
                        selected_index = choices.index(value)
                    except ValueError:
                        selected_index = choices.index(default_value)

                    x_items.append({'info' : key,
                        'button_type' : 'toggle',
                        'toggle_items' : choices,
                        'selected_item' : selected_index})
            if len(x_items) > 0:
                item_group = {'heading' : k, 'items' : x_items}
                menu.add_group(item_group)
        '''
        theme_mgr = ThemeManager()
        available_themes = theme_mgr.get_theme_names(os.path.join(self.core.app_dir, 'media', 'themes'))

        if self.theme_name in available_themes:
            selected_theme = available_themes.index(self.theme_name)
        else: selected_theme = 0

        '''



    def save(self, args=None):
        args[0].save()
        self.config.write()
        if args[1] == 'quit':
            soya.quit()
            restart_program()
            #self.core._start()  # starts recursive a new core needs better solution (reload)
