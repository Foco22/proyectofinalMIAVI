import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import urllib.request  # we are going to need to generate a Request object
from bs4 import BeautifulSoup as soup

################ Web - Scraping ########################

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'}
pagina = 'https://www.transfermarkt.com'
url = 'https://www.transfermarkt.com/primera-division-de-chile/startseite/wettbewerb/CLPD/plus/?saison_id='
season = '2021'

def league_script(season,url):

    my_url = url + season
    req = urllib.request.Request(url=my_url, headers=headers)

    with urllib.request.urlopen(req) as response:
        page_html = response.read()
    
    response = BeautifulSoup(page_html).find_all('div', class_ = 'responsive-table')
    odd = response[0].find_all('tr', class_ = 'odd')
    even = response[0].find_all('tr', class_ = 'even')

    even_list = []
    odd_list = []

    for x in odd:    
        odd_team = str(x.find_all('td', class_ ='zentriert no-border-rechts')[0]).split('"')
        web = pagina + odd_team[3]
        equipo = odd_team[5]
        tupla = (equipo,web,season)
        odd_list.append(tupla)
    
    for x in even:    
        even_team = str(x.find_all('td', class_ ='zentriert no-border-rechts')[0]).split('"')
        web = pagina + even_team[3]
        equipo = even_team[5]
        tupla = (equipo,web,season)
        even_list.append(tupla)

    total_list = odd_list + even_list
    df_season = pd.DataFrame(total_list, columns = ['team','team_web','season'])
    return df_season



def league_script_team(season,url):

    
    df_season = league_script(season,url)
    df_web = pd.DataFrame()

    for x in range(len(df_season)):
        my_url = df_season.iloc[x,1]
        season = df_season.iloc[x,2]
        team = df_season.iloc[x,0]
        print(my_url)
        req = urllib.request.Request(url=my_url, headers=headers)
        with urllib.request.urlopen(req) as response:
            page_html = response.read()
    
        response = BeautifulSoup(page_html).find_all('div', class_ = 'responsive-table')
        even = response[0].find_all('tr', class_ = 'even')
    
        even_list = []
        odd_list = []
        
        for x in even:
            name_player = str(x.find_all('td', class_ = 'posrela')[0].find_all('div',class_ ='di nowrap')[0]).split('title="')[1].split('"')[0]
            name_position = str(x).split('<td>')[1].split('<')[0]
            try: 
                market_player = str(x.find_all('td', class_ = 'rechts hauptlink')[0]).split('€')[1].split('<')[0]
            except:
                market_player = '0'
            player_country = str(x.find_all('td', class_ ='zentriert')[2].find_all('img')[0]).split('title')[1].split('"')[1]
            tupla = (name_player,name_position,market_player,player_country,season,team)
            even_list.append(tupla)
       
        odd = response[0].find_all('tr', class_ = 'odd')

        for x in odd:
            name_player = str(x.find_all('td', class_ = 'posrela')[0].find_all('div',class_ ='di nowrap')[0]).split('title="')[1].split('"')[0]
            name_position = str(x).split('<td>')[1].split('<')[0]
            try: 
               market_player = str(x.find_all('td', class_ = 'rechts hauptlink')[0]).split('€')[1].split('<')[0]
            except:
               market_player = '0'
        player_country = str(x.find_all('td', class_ ='zentriert')[2].find_all('img')[0]).split('title')[1].split('"')[1]
        tupla = (name_player,name_position,market_player,player_country,season,team)
        odd_list.append(tupla)

        total_list = odd_list + even_list
        df = pd.DataFrame(total_list, columns = ['name','position','market_value','country','season','team'])
        df_web = pd.concat([df_web,df], axis = 0)
    return df_web
    
    
#print(league_script_team(season,url))