import sys
import json
import pytest
import requests
import urllib3
from pytest_localserver import plugin

import async_fakenames as app
import models


httpsserver = plugin.httpsserver    


def test_fetch_fakename(httpsserver):
    content = r'{"name":"Mrs. Neva Hessel","address":"042 Connelly Estates Suite 908\nNorth Kennedy, CT 15663","latitude":-14.154932000000002,"longitude":-76.588392,"maiden_name":"Bosco","birth_data":"1982-10-24","phone_h":"(229)290-7046x023","phone_w":"1-322-955-7206","email_u":"doyle.hettinger","email_d":"bankomatt.ru","username":"mkessler","password":"|+Nwz\"Cym0fuPFBw","domain":"stehr.info","useragent":"Mozilla\/5.0 (compatible; MSIE 10.0; Windows NT 6.0; Trident\/4.0)","ipv4":"36.238.20.204","macaddress":"AC:0D:86:6B:53:35","plasticcard":"5348836060551923","cardexpir":"07\/19","bonus":10,"company":"Rippin, Ruecker and Ankunding","color":"silver","uuid":"30c8b076-0553-3b67-980b-ea24c814cb02","height":171,"weight":94.2,"blood":"A\u2212","eye":"Amber","hair":"Straight, Black","pict":"9female","url":"https:\/\/api.namefake.com\/english-united-states\/female\/fd0a926717460996a50cbebbb4871273","sport":"Sailing","ipv4_url":"\/\/myip-address.com\/ip-lookup\/36.238.20.204","email_url":"\/\/emailfake.com\/bankomatt.ru\/doyle.hettinger","domain_url":"\/\/myip-address.com\/ip-lookup\/stehr.info"}'
    headers = {'content-type': 'text/html; charset=UTF-8'}
    httpsserver.serve_content(content, headers=headers)

    with requests.Session() as session:
        session.verify = False
        name_obj = app.fetch_fakename(session, httpsserver.url)

    assert json.loads(content).get('name') == name_obj.fullname
