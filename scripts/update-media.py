#!/usr/bin/env python
"""
$Id$
Downloads themes and music from the homepage
"""

import base64
import md5
import os
import tarfile
import urllib2


class File(object):
	def __init__(self, filename):
		self.__filename = filename

	def readlines(self):
		f = file(self.__filename, 'r')
		d = f.readlines()
		f.close()
		return d

	def write(self, data):
		f = file(self.__filename, 'wb')
		f.write(data)
		f.close()

	def md5sum(self):
		f = file(self.__filename, 'rb')
		md5sum = md5.new()
		while True:
			d = f.read(1024)
			if len(d) is 0:
				break
			md5sum.update(d)

		f.close()
		return md5sum.hexdigest()


class Directory(object):
	def __init__(self, directory):
		self.__directory = directory

	def make(self):
		if not os.path.exists(self.__directory):
			os.mkdir(self.__directory)
		elif os.path.isfile(self.__directory):
			raise OSError('ERROR: a file with the same ' \
				'name as the desired dir, "%s", ' \
				'already exists.' % self.__directory)

	def change(self):
		os.chdir(self.__directory)


class Internet(object):
	def __init__(self, username = None, password = None):
		self.__username, self.__password = username, password

	def _getData(self, request):
		u = urllib2.urlopen(request)
		d = u.read()
		u.close()
		return d

	def download(self, remote, local = None):
		if local is None: local = remote.split('/')[-1]

		print 'Dowloading %s' % remote
		request = urllib2.Request(remote)

		if self.__username:
			request.add_header('Authorization', 'Basic %s' %
				base64.encodestring('%s:%s' % (
				self.__username, self.__password))[:-1])

		File(local).write(self._getData(request))


def download(url, directory, username = None, password = None):
	MD5SUMS, TMP  = 'MD5SUMS', 'tmp'

	Directory(TMP).make()
	Directory(TMP + os.path.sep + directory).make()
	Directory(TMP + os.path.sep + directory).change()

	if os.path.isfile(MD5SUMS): os.unlink(MD5SUMS)

	internet = Internet(username, password)
	try:
		internet.download(url + MD5SUMS)
	except urllib2.URLError:
		print 'File not found or server down?'
		return False
	except urllib2.HTTPError:
		print 'Wrong password?'
		return False

	for line in File(MD5SUMS).readlines():
		(md5sum, filename) = line.split()
		print('Checking (%s) %s' % (md5sum, filename))

		if not os.path.isfile(filename):
			print '%s not found.' % filename
			internet.download(url + filename)

		print '\tProcessing %s' % filename
		if File(filename).md5sum() == md5sum:
			tar = tarfile.open(filename, mode = 'r:gz')
			for m in tar.getmembers():
				tar.extract(m,
					('..' + os.path.sep) * 2 + directory)
			print '\t\tUnpacked.'
		else:
			print '\t\tChecksum doesn\'t match. Giving up...'

	Directory('..' + os.path.sep + '..').change()


if __name__ == '__main__':
	username, password = None, None

	username = raw_input('Username: ')
	password = raw_input('Password: ')

	url = 'http://www.canta-game.org/downloads'
	download(url + '/themes/', 'themes')

	for directory in ['unfree', 'free', 'tests']:
		download(url + '/songs/' + directory + '/', 'songs',
			username, password)

