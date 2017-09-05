from bs4 import BeautifulSoup
import requests

def scrape(url, selector):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    return soup.select(selector)[0].text.strip('˚°F')

wxtemp1 = scrape(
    'http://forecast.weather.gov/MapClick.php?lat=40.7387&lon=-74.1955',
    '#current_conditions-summary > p.myforecast-current-lrg'
)
wxtemp2 = scrape(
    'https://www.wunderground.com/weather/us/nj/07103---newark/07103',
    '#curTemp > span > span.wx-value'
)
wxtemp3 = scrape(
    'https://darksky.net/forecast/40.7387,-74.1955/us12/en',
    '#title > span.currently > span.desc.swap > span.temp.swip'
)
wxtemp4 = scrape(
    'https://www.accuweather.com/en/us/newark-nj/07103/current-weather/2702_pc',
    '#detail-now > div > div.forecast > div.info > div > span.large-temp'
)

print(wxtemp1)
print(wxtemp2)
print(wxtemp3)
print(wxtemp4)