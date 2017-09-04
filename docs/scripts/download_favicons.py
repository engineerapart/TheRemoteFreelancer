#!python3
"""
This script downloads the favicons
Usage:

    python3 update_alexa path/to/data.csv
"""

import csv
import sys
import os
from urllib.parse import urlparse
import requests

def main(url):
	url_parts = urlparse(url)
	with open(url_parts.netloc + ".ico", 'wb') as f:
		response = None
		try:
			url = url_parts.scheme + '://' + url_parts.netloc + "/favicon.ico"
			print(url)
			response = requests.get(
				"https://realfavicongenerator.p.mashape.com/favicon/icon", 
				params={'platform': 'desktop', "site": url},
				headers={'X-Mashape-Key': os.environ.get("mashape_key")}
			)
		except:
			pass
		if response:
			f.write(response.content)

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print(__doc__)
		exit(1)
	with open(sys.argv[1], 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		output = list(reader)
	for row in output:
		main(row['url'])
