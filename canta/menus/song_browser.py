from browser import MenuBrowser
from canta.song.song_editor import SongEditor

class SongBrowser(MenuBrowser):

    def __init__(self, song_managers, default_manager, widget_properties, \
            use_pil=False, preview=False, octave=False, player=None, debug=False, start_screen=None):
        MenuBrowser.__init__(self, song_managers, default_manager, widget_properties, \
            use_pil, preview, octave, player, start_screen, debug)
        if len(self.browsable_items) > 0:
            self.start_button.function = start_screen.show
            self.start_button.args = [self.browsable_items[ \
                self.browsable_items.keys()[self.current_entry]], self.widgets]

