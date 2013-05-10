import os, sys

from distutils.core import setup
from distutils.version import StrictVersion
from glob import glob

def get_files(path):
    files = []
    elements = glob(path + '/*')
    for elem in elements:
        if os.path.isdir(elem):
            files.extend(get_files(os.path.join(elem)))
        else:
            files.append(os.path.join(elem))
    return files

data_dirs = ('locale', 'misc')

data_files = []
for data_dir in data_dirs:
    data_files.extend(get_files(data_dir))

setup_data_files = []
for file in data_files:
    setup_data_files.append(('share/games/canta/'+os.path.dirname(file), [file]))

setup_data_files.append(('share/games/canta/', ['run_canta', 'run_song_generator', 'run_view_theme']))
setup_data_files.append(('share/pixmaps', ['misc/canta.png', 'misc/csg.png']))
setup_data_files.append(('share/applications', ['misc/canta.desktop', 'misc/csg.desktop']))
setup_data_files.append(('share/games/canta/misc', ['misc/configspec']))
#setup_data_files.append(('games/bin', ['starter/canta', 'starter/csg']))

dirs = []
elements = glob('canta/*')
for elem in elements:
    if os.path.isdir(elem):
        dirs.append(elem)



dirs.append('canta')
dirs.append('canta.event.subjects')
dirs.append('canta.event.observers')



setup(	name = 'canta',
    description = "Canta is a 3D karaoke plattform for fun and education",
    url = "http://www.canta-game.org",
    packages = dirs,
    #packages = find_packages(),
    package_dir={'canta': 'canta'},
    scripts = ['starter/canta', 'starter/csg'],
        author="Andreas Kattner, Felix R. Lopez, Stefan Huchler",
        author_email="andreas@canta-game.org, felix@canta-game.org, stefan@canta-game.org",
    data_files = setup_data_files,
)
