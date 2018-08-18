import requests
from bs4 import BeautifulSoup
from itertools import cycle
from datetime import datetime
import pandas as pd

data_path = r"C:\Users\MV\Documents\Code\DJCal\data"
country = 'us'
state = 'massachusetts'
month = '2018-10'
base_url = 'https://www.residentadvisor.net'
events_url = '{base_url}/events/{country}/{state}/month/{month}-01'.format(base_url=base_url, country=country, state=state, month=month)

sourceCode = requests.get(events_url).text
soup = BeautifulSoup(sourceCode, 'html.parser')
events_ul = soup.find('ul', {'id': 'items'})
event_dates = events_ul.find_all('p', {'class': 'eventDate date'})
event_details = events_ul.find_all('h1', {'class': 'event-title'})


event_dates = [x.find('span').string.strip('/').split(',')[-1].strip() for x in event_dates]

data = []
for link in event_details:
    data.append([link.find('a').string, 
    base_url + link.find('a')['href']])

for i, val in enumerate(data):
    url = val[1]
    sourceCode = requests.get(url).text
    soup = BeautifulSoup(sourceCode, 'html.parser')
    item = soup.find('ul', {'class': 'clearfix'}).find('li').find('a').string
    item = item.strip()
    try:
        date = datetime.strptime(item, "%d %b %Y").strftime("%Y%m%d")
    except ValueError:
        date = item

    val.insert(0, date)
    
df = pd.DataFrame(data=data, columns=('Date', 'Event', 'Link'))
df.to_csv("{}\{}_DJListings.csv".format(data_path, month), index=False)