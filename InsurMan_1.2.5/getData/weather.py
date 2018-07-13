#coding:utf-8
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

def getWeather():
    apikey = 'CWB-9235AD3D-6C52-46BB-8BE6-D22D5AF00A7B'
    dataid = 'O-A0001-001'
    url = 'http://opendata.cwb.gov.tw/opendataapi?dataid=' + dataid + '&authorizationkey=' + apikey
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")
    locations = soup.findAll("location")
    temp = locations[0].findAll('weatherelement')[3].find('value').text

    return temp
