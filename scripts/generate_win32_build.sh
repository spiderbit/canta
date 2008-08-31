#!/bin/bash

###    TODO
#
# Installer generation would be nice
# adding Logo the Logo to the exe
# renaming main.exe to canta.exe?
# this could be moved to a build-directory or something like that?
# Soya and Pygame have a SDL.dll at the moment pygame version is used by this script, is there a problem with that?


###    The following lines you should export manually like your path-structure  before you start this script
#
 export PY_SRC="/home/black/.wine/drive_c/Python25";
 export FREEZE_PATH="/home/black/Desktop/Downloads/cx_Freeze-3.0.3"
 export DEST_PATH="./build/win32-canta"
 export VCS_PATH="."


###    The next lines are the Code for making the win32-build

if ! test -f $VCS_PATH/tmp/MSVCP60.DLL
then
  echo -e "\n\nERROR:\tplease place MSVCP60.DLL in tmp directory and start this script again!!!\n\n";
  exit;
fi

echo "1. Freezing Canta!"
mkdir -p $DEST_PATH $VCS_PATH/dist
wine $FREEZE_PATH/FreezePython.exe --include-modules=encodings.ascii,encodings.utf_8,encodings.cp437,encodings.iso8859_1 --install-dir $DEST_PATH --target-name=canta.exe main.py;
wine $FREEZE_PATH/FreezePython.exe --include-modules=encodings.ascii,encodings.utf_8 --install-dir $DEST_PATH --target-name=csg.exe csg.py;
echo "2. Creating necessary directory's"
mkdir -p $DEST_PATH/songs $DEST_PATH/themes;
echo "3. Copy libs/dlls and other stuff"
cp -r *.txt $PY_SRC/DLLs/tcl84.dll $PY_SRC/DLLs/tk84.dll $PY_SRC/Lib/site-packages/wx-2.8-msw-unicode/wx/*.dll $PY_SRC/Lib/site-packages/pygame/*.dll $PY_SRC/Lib/site-packages/soya/*.dll $PY_SRC/Lib/site-packages/soya/data tmp/MSVCP60.DLL /home/black/.wine/drive_c/windows/system32/msvcr71.dll $DEST_PATH;
cp $VCS_PATH/songs/Bruder\ Jakob $VCS_PATH/songs/Frere\ Jacques $DEST_PATH/songs -r;
cp $VCS_PATH/themes/ $DEST_PATH/ -r;
cp $VCS_PATH/locale $DEST_PATH -r;
cp $VCS_PATH/VERSION $VCS_PATH/media/*.ico $DEST_PATH;
cp $VCS_PATH/media $DEST_PATH -r;
#echo "         " DONE $DEST_PATH created \!\!



