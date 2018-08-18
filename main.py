import requests
from bs4 import BeautifulSoup
from itertools import cycle
from datetime import datetime
import pandas as pd

data_path = r"C:\Users\MV\Documents\Code\DJCal\data"
country = 'us'
state = 'massachusetts'
month = '2018-09'
base_url = 'https://www.residentadvisor.net'
events_url = '{base_url}/events/{country}/{state}/month/{month}-01'.format(base_url=base_url, country=country, state=state, month=month)

sourceCode = requests.get(events_url).text
soup = BeautifulSoup(sourceCode, 'html.parser')
events_ul = soup.find('ul', {'id': 'items'})
events_list = events_ul.find_all('li')

data = []
for item in events_list:
    if item.has_attr('class'):
        date = item.find('article').find('span').find('time').string
        date = date.split('T')[0]
        event_title = item.find('article').find('div', {'class': 'bbox'}).find('h1', {'class': 'event-title'}).find('a').string
        event_location = item.find('article').find('div', {'class': 'bbox'}).find('span').find('a').string 
        event_url = base_url + item.find('article').find('div', {'class': 'bbox'}).find('h1', {'class': 'event-title'}).find('a')['href']
    
        data.append((date, event_title, event_location, event_url))

print(data)

df = pd.DataFrame(data=data, columns=('Date', 'Event', 'Location', 'Link'))
df.to_csv("{data_path}\{month}_{state}_DJListings.csv".format(data_path=data_path, month=month, state=state), index=False)