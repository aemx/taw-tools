from bs4 import BeautifulSoup
import numpy as np
import requests

def wprint(string):
    return '\033[1;37m' + string + ': \033[0m'

def mean(li):
    return int(round(np.mean(li)))

def scrape(url, selector, chars):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'lxml')
        select = soup.select(selector)
        try:
            return (select[0].text).strip(chars)
        except IndexError:
            return (select.text).strip(chars)
    except:
        wprint('Something went wrong')
        
wx_rtmpAr = [float(scrape(
    'https://forecast.weather.gov/MapClick.php?lat=40.7387&lon=-74.1955',
    '#current_conditions-summary > p.myforecast-current-lrg', '°F'
)), float(scrape(
    'https://www.wunderground.com/personal-weather-station/dashboard?ID=KNJNEWAR10',
    '#curTemp > span > span.wx-value', ''
)), float(scrape(
    'https://darksky.net/forecast/40.7387,-74.1955',
    '#title > span.currently > span.desc.swap > span.temp.swip', '˚'
)), float(scrape(
    'https://www.accuweather.com/en/us/newark-nj/07103/current-weather/2702_pc',
    '#detail-now > div > div.forecast > div.info > div > span.large-temp', '°'
))]

wx_rtmp = mean(wx_rtmpAr)

wx_stat = scrape(
    'https://forecast.weather.gov/MapClick.php?lat=40.7387&lon=-74.1955',
    '#current_conditions-summary > p.myforecast-current', ''
)

wx_atmpAr = [float(scrape(
    'https://www.wunderground.com/personal-weather-station/dashboard?ID=KNJNEWAR10',
    '#curFeel > span.wx-data > span.wx-value', ''
)), float(scrape(
    'https://www.accuweather.com/en/us/newark-nj/07103/current-weather/2702_pc',
    '#detail-now > div > div.forecast > div.info > div > span.small-temp', 'aeFlR®°'
))]

wx_atmp = mean(wx_atmpAr)

wx_windAr = [float(scrape(
    'https://www.wunderground.com/personal-weather-station/dashboard?ID=KNJNEWAR10',
    '#windCompassSpeed > h4 > span', ''
)), float(scrape(
    'https://darksky.net/forecast/40.7387,-74.1955',
    '#currentDetails > div.wind > span.val.swap > span.num.swip', ''
))]

print('\n' + \
wprint('Currently') + str(wx_rtmp) + '°F ╱ ' + wx_stat + '\n' + \
wprint('Feels like') + str(wx_atmp) + '°F' + '\n' + \
wprint('Wind speed') + str(wx_windAr) + ' mph' + \
'\n')