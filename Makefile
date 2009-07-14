default: help

clean:
	find . -name '*.pyc' -delete
	find . -name '*~' -delete
	find . -name '*.pyo' -delete
	find locale -name 'canta-new*' -delete
	-rm dist  -r
	-rm MANIFEST

run:
	python run_canta

install:
	python setup.py install

help:
	@echo "\nMakefile options are:\n"
	@echo "	clean:		clean temporary files"
	@echo "	run:		to start canta"
	@echo "	install:	to install canta to /usr"
	@echo "\n"
