from bs4 import BeautifulSoup
import numpy as np
import requests

def wprint(string):
    return '\033[1;37m' + string + '\033[0m\n'

def scrape(url, selector, datatype, chars):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'lxml')
        select = soup.select(selector)
        try:
            return datatype((select[0].text).strip(chars))
        except IndexError:
            return datatype((select.text).strip(chars))
    except:
        wprint('Something went wrong')

def mean(li):
    return int(round(np.mean(li)))

def clean(li, li_ignore):
    for idx, val in enumerate(li_ignore):
        del li[idx]
        del li[idx]
    del li[0]
    return li

def tr_air(iata):
    status = (scrape(
        'https://www.flightview.com/airport/' + iata + '/delay',
        '#airportPage > div.status-box.gray > div.status-box-body > div > p > span', str, '\n'
    ).replace('	', '')).splitlines()[1]

    if status == 'Normal':
        return 'currently experiencing minimal delays of less than 15 minutes'
    elif status == 'Minor Delays' or 'Advisory':
        return 'currently experiencing minor delays of 30 minutes'
    elif status == 'Major Delays':
        return 'currently experiencing major delays in excess of 45 minutes'
    else:
        return 'currently closed until further notice'

def Ptr_air():
    if tr_air('EWR') == tr_air('JFK') == tr_air('LGA'):
        endstr = 'all local metropolitan airports are ' + tr_air('EWR') + '.'
    elif tr_air('EWR') != tr_air('JFK') == tr_air('LGA'):
        endstr = 'Newark International is ' + tr_air('EWR') + ',\n' + \
        'while JFK and La Guardia are ' + \
        tr_air('JFK').replace('currently ', '') + '.'
    elif tr_air('JFK') != tr_air('LGA') == tr_air('EWR'):
        endstr = 'JFK is ' + tr_air('JFK') + ',\n' + \
        'while La Guardia and Newark International are ' + \
        tr_air('LGA').replace('currently ', '') + '.'
    elif tr_air('LGA') != tr_air('EWR') == tr_air('JFK'):
        endstr = 'La Guardia is ' + tr_air('LGA') + ',\n' + \
        'while Newark International and JFK are ' + \
        tr_air('EWR').replace('currently ', '') + '.'
    else:
        endstr = 'Newark International is ' + tr_air('EWR') + ',\n' + \
        'JFK is ' + tr_air('JFK').replace('currently ', '') + ',\n' + \
        'and La Guardia is ' + tr_air('LGA').replace('currently ', '') + '.'

    return 'If you’re looking to catch a flight today, ' + endstr

def Pwx_all():
    if wx_wind >= 25:
        wx_wist = ' with wind'
    elif wx_wind >= 15:
        wx_wist = ' with light wind'
    else:
        wx_wist = ''

    wx_fore = ''

    for idx, val in enumerate(wx_foreAr):
        if idx % 2 == 0:
            wx_fore += '\n' + val + ' ... '
        else:
            wx_fore += val + ' '
            
    return 'Currently, it is ' + wx_stat + wx_wist + \
    ' in Newark with a temperature of ' + wx_temp + '.' + wx_fore

wx_tempAr = [scrape(
    'https://forecast.weather.gov/MapClick.php?lat=40.7387&lon=-74.1955',
    '#current_conditions-summary > p.myforecast-current-lrg', float, '°F'
), scrape(
    'https://www.wunderground.com/personal-weather-station/dashboard?ID=KNJNEWAR10',
    '#curTemp > span > span.wx-value', float, ''
), scrape(
    'https://darksky.net/forecast/40.7387,-74.1955',
    '#title > span.currently > span.desc.swap > span.temp.swip', float, '˚'
), scrape(
    'https://www.accuweather.com/en/us/newark-nj/07103/current-weather/2702_pc',
    '#detail-now > div > div.forecast > div.info > div > span.large-temp', float, '°'
)]

wx_temp = str(mean(wx_tempAr)) + ' degrees'

wx_stat = scrape(
    'https://forecast.weather.gov/MapClick.php?lat=40.7387&lon=-74.1955',
    '#current_conditions-summary > p.myforecast-current', str, ''
).lower()

wx_windAr = [scrape(
    'https://www.wunderground.com/personal-weather-station/dashboard?ID=KNJNEWAR10',
    '#windCompassSpeed > h4 > span', float, ''
), scrape(
    'https://darksky.net/forecast/40.7387,-74.1955',
    '#currentDetails > div.wind > span.val.swap > span.num.swip', float, ''
)]

wx_wind = mean(wx_windAr)

wx_foreRaw = scrape(
    'https://forecast.weather.gov/MapClick.php?lat=40.7387&lon=-74.1955',
    '#detailed-forecast-body', str, ''
).lstrip('\n')

days_all = [
    'This Afternoon', 'Tonight', 'Saturday', 'Sunday',
    'Monday', 'Tuesday', 'Wednesday', 'Thursday'
]

days_ignore = [
    'This Afternoon', 'Monday Night', 'Tuesday', 'Tuesday Night',
    'Wednesday', 'Wednesday Night', 'Thursday'
]

for day in days_all:
    wx_foreRaw = wx_foreRaw.replace(day, '$' + day + '$')

wx_foreRaw = wx_foreRaw.replace('$ Night', ' Night$')
wx_foreRaw = wx_foreRaw.replace('  ', ' ')
wx_foreRaw = wx_foreRaw.replace('. $', '.$')
wx_foreAr = wx_foreRaw.split('$')
wx_foreAr = clean(wx_foreAr, days_ignore)

print('\n' + wprint('FLIGHT INFORMATION') + Ptr_air() + '\n')
print(wprint('CURRENT WEATHER') + Pwx_all() + '\n')