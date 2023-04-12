import numpy as np
import pandas as pd
from dotenv import dotenv_values
import requests
import re
import math
from statistics import mean

config = dotenv_values(".env")

def ua_category(user_agent):
  if isinstance(user_agent, str):
    response = requests.get("https://api.apicagent.com/?ua=" + user_agent)
    if 'category' in response.json().keys():
      return 0 #bot
    else:
      if 'client' in response.json().keys():
        return 1 #human
      else:
        return 2 #unknown
  else:
    return 2 #unknown


def ip_info2(ip):
    response = requests.get("http://sigetilt.bget.ru/?ip=" + ip)
    if 'asn' in response.json().keys() and response.json()['asn'] != False:
        word = response.json()['asn'].lower()
        regexp = re.compile('yandex|google')
        if regexp.search(word):
            asn = 0  # bot
        else:
            asn = 1  # human
    else:
        asn = 2  # unknown

    if 'proxy' in response.json().keys():
        if (response.json()['proxy'] == 'yes'):
            proxy = 1
        else:
            proxy = 0
    else:
        proxy = 0

    if (response.json()['region'] == False):
        latitude = 0
        longitude = 0
    else:
        if 'latitude' in response.json()['region'].keys() and 'longitude' in response.json()['region'].keys():
            latitude = response.json()['region']['latitude']
            longitude = response.json()['region']['longitude']
        else:
            latitude = 0
            longitude = 0

    return [latitude, longitude, asn, proxy]


def ip_info(ip):
    # return [0, 0, 0, 0]
    response = requests.get("https://proxycheck.io/v2/" + ip + "?key="+config['KEY']+"&vpn=1&asn=1")
    if 'asn' in response.json().keys() and response.json()[ip]['asn'] != False:
        word = response.json()['asn'].lower()
        regexp = re.compile('yandex|google')
        if regexp.search(word):
            asn = 0  # bot
        else:
            asn = 1  # human
    else:
        asn = 2  # unknown

    if 'proxy' in response.json().keys():
        if (response.json()[ip]['proxy'] == 'yes'):
            proxy = 1
        else:
            proxy = 0
    else:
        proxy = 0

    if (response.json()[ip]['latitude'] == False):
        latitude = 0
        longitude = 0
    else:
        if 'latitude' in response.json()[ip].keys() and 'longitude' in response.json()[ip].keys():
            latitude = response.json()[ip]['latitude']
            longitude = response.json()[ip]['longitude']
        else:
            latitude = 0
            longitude = 0

    return [latitude, longitude, asn, proxy]


def moving_avg(x, n):
 cumsum = np.cumsum(np.insert(x, 0, 0))
 return (cumsum[n:] - cumsum[:-n]) / float(n)

def avg_ceil(arr):
  return math.ceil( sum(arr) / len(arr))
