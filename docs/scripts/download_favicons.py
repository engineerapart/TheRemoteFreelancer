#!python3
"""
This script downloads the favicons
Usage:

    python3 update_alexa path/to/data.csv
"""

import os
import requests

favicon_path = os.path.join(os.path.dirname(__file__), "..", "icons")


def download_favicons(links):
    for link in links:
        netloc = link['netloc']
        url = 'http://' + netloc
        new_favicon_path = os.path.join(favicon_path, netloc + ".ico")
        if not os.path.exists(new_favicon_path):
            try:
                print(url)
                response = requests.get(
                    "https://realfavicongenerator.p.mashape.com/favicon/icon",
                    params={'platform': 'desktop', "site": url},
                    headers={'X-Mashape-Key': os.environ.get("mashape_key")}
                )
            except:
                pass
            else:
                if response:
                    with open(new_favicon_path, 'wb') as f:
                        f.write(response.content)
