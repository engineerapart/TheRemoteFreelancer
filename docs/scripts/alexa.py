import hmac, hashlib, base64, collections, urllib.parse, urllib.error, os
import requests
from datetime import datetime, timedelta
import re
import xml.etree.ElementTree as ET

rank_search = re.compile("<aws:Rank>(.*?)</aws:Rank>")

def get_awi_url_info(url, when): 

    access_key = os.environ.get("access_key")
    secret_key = os.environ.get("secret_key")
    service_host = "awis.amazonaws.com"

    # 
    params = {
      'Action': 'UrlInfo',
      'AWSAccessKeyId' : access_key,
      'ResponseGroup': 'Rank',
      'SignatureMethod': 'HmacSHA256',
      'SignatureVersion': '2',
      'Start': when.strftime('%Y-%m-%d'),
      'Range': '1',
      'Timestamp': datetime.utcnow().isoformat(),
      'Url': url
    }

    ordered_params = collections.OrderedDict(sorted(params.items()))

    query_params = "&".join([ "%s=%s" % (k, urllib.parse.quote(v,'[^A-Za-z0-9\-_.~]')) for k,v in ordered_params.items()])

    # Signing Key
    data = "GET\n" + service_host.lower() + "\n/\n" + query_params
    data_hash = hmac.new(secret_key.encode("utf-8"), data.encode("utf-8"), hashlib.sha256).digest()
    data_base64 = base64.b64encode(data_hash).strip()
    signed = urllib.parse.quote(data_base64,'[^A-Za-z0-9\-_.~]')

    query_url = "http://awis.amazonaws.com/?%s&Signature=%s" % (query_params, signed)

    result = requests.get(url=query_url)
    return ET.fromstring(result.content)

def rank_when(url, when):
  result = get_awi_url_info(url, when).findtext(".//{http://awis.amazonaws.com/doc/2005-07-11}Rank")
  if result:
    return int(result)
  else:
    return float('inf')


def get_rank_change(url):
  a_month_ago = datetime.utcnow() - timedelta(days=33)
  now = datetime.utcnow() - timedelta(days=3)
  url_without = url.replace("www.", "")
  if "www." in url:
    return min(rank_when(url_without, now), rank_when(url, now))
  else:
    return rank_when(url, now)



