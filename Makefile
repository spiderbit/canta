clean:
	find . -name '*.pyc' -delete
	find . -name '*~' -delete
	find . -name '*.pyo' -delete
	find locale -name 'canta-new*' -delete
#	-rm build -r
	-rm dist  -r
	-rm MANIFEST
	
run:
	python main.py

install:
	python setup.py install

sdist:
	python setup.py sdist --formats=tar
	7z a dist/canta-`cat VERSION`.tar.7z dist/canta-`cat VERSION`.tar

exe:
	cp media/canta.ico .
	scripts/generate_win32_build.sh
	makensis -Dversion=`cat VERSION` installer.nsi
	-rm build canta.ico -rf

#distribute: clean	
#	tar cvjf ../canta.tbz2 ../gui


md5:
	-cd dist; md5sum *.7z *.exe > canta-`cat ../VERSION`.md5; fi

help:
	@echo "\nMakefile options are:\n"
	@echo "	clean:		clean temporary files"
	@echo "	run:		to start canta"
	@echo "	install:	to install canta to /usr"
	@echo "	sdist:		to generate a tar.gz archive or zip(windows)"
	@echo "	exe:		to generate a windows installer"
	@echo "			WARNING: u need to install stuff and edit"
	@echo "			generate_win32_build.sh before it will work"
	@echo "\n"

