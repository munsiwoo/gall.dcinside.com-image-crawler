import urllib.request
from requests import get as request
from itertools import chain
from random import shuffle
from re import findall
from os import stat, remove
from glob import glob
# dcinside gallery image parser
# made by munsiwoo

def random_filename() : # random file name
	char_list = [chr(x) for x in range(65, 91)] + [chr(x) for x in range(97,123)]
	shuffle(char_list)
	return (''.join(char_list))[0:10] + '.png'

def garbage_collector() : # delete logo image
	files = glob('images/*')
	for x in files :
		file = stat(x)
		if(file.st_size == 3795) :
			remove(x)

def get_image_uri(uri_list) : # get image uri
	global headers

	image_list = list()
	regex = "<img\s[^>]*?src\s*=\s*['\"]([^'\"]*?viewimage[.]php[^'\"]*?)['\"][^>]*?>"
	# src : http://dcimg8.dcinside.co.kr/viewimage.php?id=0&no=0

	print("collecting image uri..")

	for x in uri_list :
		uri = 'http://gall.dcinside.com{}'.format(x)
		html = request(uri, headers=headers).text
		image_list.append(findall(regex, html))
		
	print("end")
	image_list = list(chain(*image_list))	

	return image_list

def get_content_list(gall, page) : # get content list
	global headers

	uri  = 'http://gall.dcinside.com/board/lists/?id={}&page={}'.format(gall, page)	
	regex = '\/board\/view\/\?id={}&no=[\d]+'.format(gall)

	html = request(uri, headers=headers).text
	content_list = findall(regex, html)

	return content_list

def main() :
	global headers

	headers = {
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'User-Agent': 'Mozilla/5.0'
	} # headers is important

	gall_list = ['superidea'] # dcinside gallery list
	content_list = image_list = list()

	for x in range(len(gall_list)) :
		for y in range(1) : # you can set page, ex) range(1, 11)
			content_list.append(get_content_list(gall_list[x], y))

	content_list = list(chain(*content_list)) # list faltten
	image_list = get_image_uri(content_list) # get images uri
	
	opener = urllib.request.build_opener()
	opener.addheaders = [('Referer','gall.dcinside.com')] # header is important
	urllib.request.install_opener(opener)

	for image in image_list :
		filename = 'images/' + random_filename()
		try :
			print("download : " + filename)
			urllib.request.urlretrieve(image, filename)
		except urllib.error.URLError as e :
			print("failed : " + image)
			continue

	garbage_collector() # delete logo image

if __name__ == '__main__' :
	print('gall.dcinside.com image parser')
	main()
