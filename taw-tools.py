from bs4 import BeautifulSoup
import requests as reqs

wxpage = reqs.get('https://www.wunderground.com/weather/us/nj/07103---newark/07103')
wxsoup = BeautifulSoup(wxpage.text, 'lxml')
wxtemp = wxsoup.select('#curTemp > span > span.wx-value')[0].text

print(wxtemp)