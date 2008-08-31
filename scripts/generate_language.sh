#!/bin/bash
#echo "../locale/"$1
path=locale/$1/LC_MESSAGES

function bla {
  echo "Now first you have to edit the 'po'-file with text-editor or gui like poedit!"
  echo "      poedit $path/canta.po"
  echo "then to compile the file type"
  echo "      scripts/compile_languages.sh"
}

if test -n "$1"
then
  xgettext main.py --language=Python -o locale/canta.pot --force-po;
  find . -iname "*.py" -exec xgettext --language=Python -j -o locale/canta.pot --keyword=_ {} \;
  if test -d locale/$1
  then
    echo "Found existing language directory $1"
    echo "Try to merge new File with Old File!"
    echo " $1/canta-old.po"
    sleep 2
#    mv $path/canta.po $path/canta-old.po
    msginit -l $1 -o $path/canta-new.po -i locale/canta.pot
    msgmerge -U $path/canta.po $path/canta-new.po
    echo "Hopefully successfull merged"
    bla
  else
    mkdir -p $path
    msginit -l $1 -o $path/canta.po -i locale/canta.pot
    bla
  fi
  rm locale/canta.pot
else
  echo "Parameter forgotten?"
  echo "Usage example for german language:"
  echo "> $0 de_DE "
fi


