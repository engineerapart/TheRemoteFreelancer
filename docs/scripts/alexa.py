import base64
import collections
import hashlib
import hmac
import os
import re
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET

import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth

rank_search = re.compile("<aws:Rank>(.*?)</aws:Rank>")


def get_awi_url_info(url):
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    params = {
        'Action': 'UrlInfo',
        'ResponseGroup': "Rank",
        'Url': url
    }

    ordered_params = collections.OrderedDict(sorted(params.items()))

    query_params = "&".join(
        ["%s=%s" % (k, urllib.parse.quote(v, '[^A-Za-z0-9\-_.~]')) for k, v in ordered_params.items()])

    auth = AWSRequestsAuth(access_key, secret_key, "awis.us-west-1.amazonaws.com", 'us-west-1', 'awis')

    query_url = f"https://awis.us-west-1.amazonaws.com/api?{query_params}"

    result = requests.get(url=query_url, auth=auth)
    return ET.fromstring(result.content)


def download_aws_rank(url):
    result = get_awi_url_info(url).findtext(".//{http://awis.amazonaws.com/doc/2005-07-11}Rank")
    if result:
        return int(result)
    else:
        return 10_000_000


def get_rank(url):
    url_without = url.replace("www.", "")
    if "www." in url:
        return min(download_aws_rank(url_without), download_aws_rank(url))
    else:
        return download_aws_rank(url)
