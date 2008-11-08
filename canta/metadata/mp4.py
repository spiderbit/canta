# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

from canta.metadata import BaseFormat
from mutagen import mp4

class MP4Format(BaseFormat):
    MutagenType = mp4.MP4
    tag_mapping = {
            'title':       '\xa9nam',
            'artist':      '\xa9ART',
            'album':       '\xa9alb',
            'genre':       '\xa9gen',
            'date':        '\xa9day',
            'tracknumber': 'trkn',
            'discnumber':  'disk',
            'copyright':   'cprt',
        }
    others = False
    writable = True
    
# vim: et sts=4 sw=4


