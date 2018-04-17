#! /usr/bin/env python3
import requests
import re
import json
import time
import sys
import urllib.parse

def main():
	'''
		QUICK AND HACKY - THERE IS CERTAINLY A BETTER WAY TO WRITE THIS
		BUT IT WORKS FOR THE USE CASE ITS INTENDED FOR

		GOD BLESS PYTHON

	'''
	rcount = 0

	base_url = 'https://74.43.119.80:2016'

	requests.packages.urllib3.disable_warnings()

	with open('last_site2.conf', 'r') as l:
		lastsite = l.read().splitlines()
		lstring = '\n'.join(lastsite)

	urls = {}

	count = 0

	for line in lastsite:
		try:
			response_code = re.findall('\\[(R=\\d+)\\,', line)
			if len(response_code) > 0:
				response_code = (response_code[0])[2::]

			url = re.findall('\\^(.[^$]*)\\$', line)
			if url != []:
				first = url[0].replace('\\', '')

			url = re.findall('\\${.*}(.*) ', line)
			if url != []:
				last = url[0].replace('\\', '')
				print (first, last)

			try:
				first, last
				urls[count] = {1:first, 2:last, 'rcode':response_code}
			except NameError:
				print('Could not determine rewrite scheme for', line)

		except Exception as e:
			print(e)

		count += 1

	print('Checking {} urls'.format(len(urls)))

	fix = []
	rth = []

	for url in urls:
		try:
			original = 'https://74.43.119.80:2016' + urls[url][1]

			r = requests.get('https://74.43.119.80:2016' + urls[url][1], verify=False, allow_redirects=False)

			expected = urls[url][2].strip()
			#print(r.status_code, r.headers['Location'])#'https://74.43.119.80:2016' + urls[url][1], r.headers)
			if r.status_code == 301:
				red1 = r.headers['Location']
				r = requests.get(r.headers['Location'], verify=False, allow_redirects=False)

			if r.status_code == 200:
				#print('One Redirect')
				#print(original)
				#print(red1)
				pass

			elif r.status_code == 301:
				red2 = r.headers['Location']
				r = requests.get(r.headers['Location'], verify=False, allow_redirects=False)

				# 2 Redirects
				if r.status_code == 200:
					print(rcount, 'Replace---')
					original = original.replace('https://74.43.119.80:2016','')
					red1 = red1.replace('https://74.43.119.80:2016','')
					red2 = red2.replace('https://74.43.119.80:2016','')
					print(original)
					print(red1)
					print(red2, '\n\n')

					rcount += 1

					lstring = lstring.replace(red1, red2)

				# 3 or more redirects, this shouldn't happen
				elif r.status_code == 301:
					print('3 Or More Redirects')
			with open('outfile.conf', 'w') as o:
				o.write(lstring)
		except Exception as e:
			print(e, url)

		time.sleep(0.2)



	
if __name__ == '__main__':
	main()
