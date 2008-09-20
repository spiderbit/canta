from browser import MenuBrowser

class SongEditorBrowser(MenuBrowser):

	def __init__(self, browsable_items, widget_properties, \
			use_pil=False, preview=False, octave=False, player=None, debug=False, start_screen=None):
		MenuBrowser.__init__(self, browsable_items, widget_properties, \
			use_pil, preview, octave, player, debug)

		self.l_start = 'Edit'
		self.start_screen=start_screen

		if len(self.browsable_items) > 0:
			self.start_button.args = [self.browsable_items[self.selected], self.widgets]
			self.start_button.function = self.clean_start

	def clean_start(self, args):
		self.stop_preview()
		if len(self.browsable_items) > 0:
			self.start_screen.show(args)
		
