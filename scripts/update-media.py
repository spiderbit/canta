
import os
import md5
import tarfile

class MyWeb:
    def __init__(self, host, webuser=None, webpass=None):
        self.host = host
        self.webuser = webuser
        self.webpass = webpass

    def download_file(self, web_file, lokal_file=None):
        """
        Downloads a file
        """

        import urllib2
        import base64

        if lokal_file == None:
            lokal_file = web_file.split('/')[-1]

        request =  urllib2.Request(self.host + '/' + web_file)

        if self.webuser:
            base64string = base64.encodestring('%s:%s' % (self.webuser, self.webpass))[:-1]
            request.add_header("Authorization", "Basic %s" % base64string)

        htmlFile = urllib2.urlopen(request)
        htmlData = htmlFile.read()
        htmlFile.close()


        f = file(lokal_file, "wb")
        f.write(htmlData)
        f.close() 






def _mkdir(newdir):
	if os.path.isdir(newdir):
		pass
	elif os.path.isfile(newdir):
		raise OSError("ERROR: a file with the same name as the desired " \
							"dir, '%s', already exists." % newdir)
	else:
		os.mkdir(newdir)

def get_hex(filex):
	m = md5.new()
	f = file(filex, 'rb') # open in binary mode
	while True:
		t = f.read(1024)
		if len(t) == 0: break # end of file
		m.update(t)
	return m.hexdigest()

def do_it(base_url, dir, target_dir, username, password):

	newdir = 'tmp'


	seperator='/'
	MD5SUMS='MD5SUMS'

	#url_path = base_url + seperator + dir + seperator
	url_path = dir + seperator
	_mkdir(newdir)
	os.chdir(newdir)
	_mkdir(dir)
	os.chdir(dir)
	if os.path.isfile(MD5SUMS):
		os.unlink(MD5SUMS)
	#os.system(dl_app +' '+ url_path + MD5SUMS)
	web = MyWeb(base_url, username, password)
	web.download_file(url_path + MD5SUMS, MD5SUMS)
	#os.system('cat' +' '+ MD5SUMS)
	md5file = file(MD5SUMS)
	lines = md5file.readlines()
	for line in lines:
		words = line.split()
		
		if not os.path.isfile(words[1]):	# path must be checked
			print "Downloading " + words[1] + ", because you don't have it ..."
			web.download_file(url_path + words[1])
			print "Done."
		elif words[0] != get_hex(words[1]):
			print "Downloading " + words[1] + ", update or corruption ..."
			os.unlink(words[1])
			web.download_file(url_path + words[1])
			print "Done."
		if words[0] == get_hex(words[1]):
			print "File " + words[1] + "\t\tis ok."
			#os.chdir('songs/')
			#print 'tar xZf ' + words[1] + ' --directory=../../' + target_dir
			tar=tarfile.open(words[1], mode="r:gz")
			#tar.makedir(tar.getmembers(),"testtttt")
			members = tar.getmembers()
			for member in members:
				tar.extract(member, "../../"+ target_dir)
				#  	map(tar.extract, tar.getmembers())
			#os.system('tar xzf ' + words[1] + ' --directory=../../' + target_dir)
			#os.chdir('../tmp/')
		else:
			print "ERROR: file  " + words[1] + " could not be synced!!!"
	os.chdir('..')
	os.chdir('..')
	#os.system('tar xzf ' + words[1])



base_url="http://www.canta-game.org/downloads/songs"
sub_urls=['unfree', 'free', 'tests']


	

username = raw_input('Username: ')
password = raw_input('Password: ')


md5_urls=[]

for dir in sub_urls:
	do_it(base_url, dir, target_dir='songs', username=username, password=password)


base_url="http://www.canta-game.org/downloads/"

do_it(base_url, dir='themes', target_dir='themes', username=username, password=password)
	
	


