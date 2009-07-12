from canta.song.song_manager import SongManager
from canta.song.song import Song, MingusSong

import os
import sys



app_dir = os.path.dirname(sys.argv[0])
#sm = SongManager(os.path.join(app_dir, 'media', 'songs'))
sm = SongManager(os.path.join('/', 'home', 'black', '.canta', 'songs'))
sm.search()
sm.verify()
sm.sort()
song = sm.get_by_title(sys.argv[1])
print sm.songs
song.read()
song.split_in_lines()
ming = MingusSong()
ming.load_from_song(song)
ming.generate_pictures()




#test_compare.setUp = setup
#test_compare.tearDown = teardown
