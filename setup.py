import os, sys
#import ez_setup
#ez_setup.use_setuptools()

#from setuptools import setup, find_packages

cmd_class = {}
if sys.argv[1] == 'bdist_debian':
    import bdist_debian
    cmd_class = {'bdist_debian': bdist_debian.bdist_debian}

from distutils.core import setup
from distutils.version import StrictVersion
#import py2exe
from glob import glob

version_file = open('VERSION')
version = version_file.next()
  

def get_files(path):
    files = []
    elements = glob(path + '/*')
    for elem in elements:
        if os.path.isdir(elem):
            files.extend(get_files(os.path.join(elem)))	
        else:
            files.append(os.path.join(elem))
    return files

data_dirs = ('locale', 'songs', 'themes', 'misc')

data_files = []
for data_dir in data_dirs:
    data_files.extend(get_files(data_dir))

setup_data_files = []
for file in data_files:
    setup_data_files.append(('share/games/canta/'+os.path.dirname(file), [file]))

setup_data_files.append(('share/games/canta/', ['ABOUT.txt', 'changelog.txt', 'HACKING.txt', 'INSTALL.txt', 'LICENSE.txt', 'main.py', 'csg.py', 'VERSION', 'configspec']))
setup_data_files.append(('share/pixmaps', ['misc/canta.png', 'misc/csg.png']))
setup_data_files.append(('share/applications', ['misc/canta.desktop', 'misc/csg.desktop']))
setup_data_files.append(('share/games/canta/misc', ['misc/HELP.txt']))


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
    cmdclass = cmd_class,
    scripts = ['starter/canta', 'starter/csg'],
        author="Andreas Kattner, Felix R. Lopez, Stefan Huchler",
        author_email="andreas@canta-game.org, felix@canta-game.org, stefan@canta-game.org",
        version = version,
    data_files = setup_data_files,
)



