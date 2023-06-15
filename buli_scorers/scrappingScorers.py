"""
Author:  LuisG
Created: January, 2023

Python script to web-scrap the goalscorer information from the DFB historic archives
"""

# imports
import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

# =============================
#    AUXILIARY FUNCTIONS
# =============================

def nation(profil_url):
    
    data_profil = requests.get(profil_url).text
    soup_profil = BeautifulSoup(data_profil, 'html.parser')
    nations_thumbs = soup_profil.find_all('img', attrs={"data-toggle": "tooltip"})
    
    if len(nations_thumbs)==0: return None
    else:
        nations = []
        for element in nations_thumbs:
            nations.append(element['title'])
    return nations

# ==============================================================================

# template for url addresses in DFB statistic data base
ADDRESS = 'https://www.dfb.de/maenner-bundesliga/statistik/rekordtorjaeger/?no_cache=1&spieledb_path=%2Fdatencenter%2F12%2Frekord-torjaeger%2F{}%3Famp%253Bspieledb_path%3D%252Fdatencenter%252F12%252Frekord-torjaeger%252F3%253Fid%253D12%2526t3_remote%253Dtrue%2526t3_uri%253Dhttps%25253A%25252F%25252Fwww.dfb.de%25252Fbundesliga%25252Fstatistik%25252Frekordtorjaeger%25252F%25253Fno_cache%25253D1%26id%3D12%26spieledb_path%3D%252Fdatencenter%252F12%252Frekord-torjaeger%252F2%253Famp%25253Bspieledb_path%253D%25252Fdatencenter%25252F12%25252Frekord-torjaeger%25252F3%25253Fid%25253D12%252526t3_remote%25253Dtrue%252526t3_uri%25253Dhttps%2525253A%2525252F%2525252Fwww.dfb.de%2525252Fbundesliga%2525252Fstatistik%2525252Frekordtorjaeger%2525252F%2525253Fno_cache%2525253D1%2526id%253D12%2526t3_remote%253Dtrue%2526t3_uri%253Dhttps%25253A%25252F%25252Fwww.dfb.de%25252Fmaenner-bundesliga%25252Fstatistik%25252Frekordtorjaeger%25252F%25253Fno_cache%25253D1%26t3_remote%3Dtrue%26t3_uri%3Dhttps%253A%252F%252Fwww.dfb.de%252Fmaenner-bundesliga%252Fstatistik%252Frekordtorjaeger%252F%253Fno_cache%253D1'

# first web page with lead scorers
dfb_urls = ['https://www.dfb.de/bundesliga/statistik/rekordtorjaeger/?no_cache=1']

# create the list of DFB web pages with the goal scorers list
for k in range(2,78):
    web_add = ADDRESS.format(k)
    dfb_urls.append(web_add)

# Defining of the dataframes
df = pd.DataFrame(columns=['Platz', 'Spieler', 'Tore', 'Elfmeter'])
df_ref = pd.DataFrame(columns=['Spieler', 'DFB_id', 'link'])

# loop through the DFB web pages
for url in dfb_urls:
    # Create a handle, page, to handle the contents of the website
    data = requests.get(url).text
    
    # Creating BeautifulSoup object
    soup = BeautifulSoup(data, 'html.parser')
    
    # Creating list with the tables
    table = soup.find('table')
    
    # Collecting Data
    for row in table.tbody.find_all('tr'):
        # Find all data for each column
        columns = row.find_all('td')
        
        if(columns != []):
            platz = columns[0].text.strip()
            spieler = columns[1].text.strip()
            tore = columns[2].text.strip()
            elfmeter = columns[3].text.strip()
        
            df.loc[len(df)] = [platz, spieler, tore, elfmeter]
            
    webs = soup.find_all(href=re.compile("datencenter.dfb.de"))
    for web in webs:
        df_ref.loc[len(df_ref)] = [web.text.strip(), web.get('href')[34:], web.get('href')]

# formatting players table
df_ref['Nation'] = df_ref['link'].apply(lambda x: nation(x))
df_ref['Nationalelf'] = df_ref['Nation'].apply(lambda x: x[0] if x is not None else None)

df_ref.to_csv('data/spielers.csv', index=False)
df.to_csv('data/scorer_table.csv', index=False)