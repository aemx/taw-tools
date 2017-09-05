from bs4 import BeautifulSoup
import numpy as np
import os
import requests

def scrape(url, selector):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    return float(soup.select(selector)[0].text.strip('˚°F'))

wx_rtmpAr = [scrape(
    'http://forecast.weather.gov/MapClick.php?lat=40.7387&lon=-74.1955',
    '#current_conditions-summary > p.myforecast-current-lrg'
), scrape(
    'https://www.wunderground.com/weather/us/nj/07103---newark/07103',
    '#curTemp > span > span.wx-value'
), scrape(
    'https://darksky.net/forecast/40.7387,-74.1955/us12/en',
    '#title > span.currently > span.desc.swap > span.temp.swip'
), scrape(
    'https://www.accuweather.com/en/us/newark-nj/07103/current-weather/2702_pc',
    '#detail-now > div > div.forecast > div.info > div > span.large-temp'
)]

wx_rtmp = int(round(np.mean(wx_rtmpAr)))
print('Current temperature: ' + str(wx_rtmp) + '°F')