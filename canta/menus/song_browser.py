from browser import MenuBrowser
from canta.song.song_editor import SongEditor

class SongBrowser(MenuBrowser):

	def __init__(self, browsable_items, widget_properties, \
			use_pil=False, preview=False, octave=False, player=None, debug=False, start_screen=None):
		MenuBrowser.__init__(self, browsable_items, widget_properties, \
			use_pil, preview, octave, player=player, debug=debug)
		if len(self.browsable_items) > 0:
			self.start_button.function = start_screen.show
			self.start_button.args = [self.browsable_items[self.selected], self.widgets]
		

		
			
