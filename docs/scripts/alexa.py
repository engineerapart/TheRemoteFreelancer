import base64
import collections
import hashlib
import hmac
import os
import re
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime

import requests

rank_search = re.compile("<aws:Rank>(.*?)</aws:Rank>")

session = None


def get_awi_url_info(url):
    global session

    access_key = os.environ.get("access_key")
    secret_key = os.environ.get("secret_key")
    service_host = "awis.amazonaws.com"

    # 
    params = {
        'Action': 'UrlInfo',
        'AWSAccessKeyId': access_key,
        'ResponseGroup': 'Rank',
        'SignatureMethod': 'HmacSHA256',
        'SignatureVersion': '2',
        'Timestamp': datetime.utcnow().isoformat(),
        'Url': url
    }

    ordered_params = collections.OrderedDict(sorted(params.items()))

    query_params = "&".join(
        ["%s=%s" % (k, urllib.parse.quote(v, '[^A-Za-z0-9\-_.~]')) for k, v in ordered_params.items()])

    # Signing Key
    data = "GET\n" + service_host.lower() + "\n/\n" + query_params
    data_hash = hmac.new(secret_key.encode("utf-8"), data.encode("utf-8"), hashlib.sha256).digest()
    data_base64 = base64.b64encode(data_hash).strip()
    signed = urllib.parse.quote(data_base64, '[^A-Za-z0-9\-_.~]')

    query_url = "http://awis.amazonaws.com/?%s&Signature=%s" % (query_params, signed)

    if not session:
        session = requests.Session()
    result = session.get(url=query_url)
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
