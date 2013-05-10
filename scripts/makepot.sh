#!/bin/bash

cd ..

echo "Creating po/canta.pot..."

A=`find . -iname "*.py"`
xgettext run_canta $A --language=Python --output=po/canta.pot --from-code=utf-8 --keyword=_

cd po

dir -1|grep -v .pot|while read PO
do
  msgmerge $PO canta.pot -o $PO
done

echo "Success."
