import requests 
import pandas as pd


################ Api Token ########################


api = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

headers = {
	"X-RapidAPI-Key": "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
	"X-RapidAPI-Host": "XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
}


################################### Extraccion League_season #########################################


def leagues_countries():

    url = "https://api-football-v1.p.rapidapi.com/v3/leagues"
    print(url)
    response = requests.request("GET", url, headers=headers)  
    response = response.json()
 
    df_league_total =  pd.DataFrame()

    for x in response['response']:
    
        id_league = x['league']['id']
        id_name = x['league']['name']
        id_type = x['league']['type']
        country_name = x['country']['name']
        tupla = [(id_league,id_name,id_type,country_name)]
        df_league = pd.DataFrame(tupla, columns = ['id_league','name_league','type_league','country_league'])
        df_league_total = pd.concat([df_league_total,df_league],axis = 0)
    
    return df_league_total


def league_season(liga,season):
    
    url = "https://api-football-v1.p.rapidapi.com/v3/teams"
    
    lista_equipos = []
    for i in season:
        querystring = {"league":liga,"season":i}
        response = requests.request("GET", url, headers=headers, params=querystring)
        response = response.json()
        for x in response['response']:
            tupla = (x['team']['id'], x['team']['name'], x['team']['country'],response['parameters']['league'],
            response['parameters']['season'])
            lista_equipos.append(tupla)
    
    df_equipos = pd.DataFrame(lista_equipos, columns = ['id','name','country','league','season'])
    return df_equipos

def league_season_team(liga,season,team):

    contador_red = 0
    contador_yellow = 0

    url = "https://api-football-v1.p.rapidapi.com/v3/teams/statistics"
    querystring = {"league":liga,"season":season,"team":team}
    response = requests.request("GET", url, headers=headers, params=querystring) 
    response = response.json()

    id_league = response['response']['league']['id']
    name_league = response['response']['league']['name']
    season_league = response['response']['league']['season']
    id_team = response['response']['team']['id']
    name_team = response['response']['team']['name']
    match_played = response['response']['fixtures']['played']['total']
    wins_played = response['response']['fixtures']['wins']['total']
    draws_played = response['response']['fixtures']['draws']['total']
    loses_played = response['response']['fixtures']['loses']['total']
    
    goals_favor = response['response']['goals']['for']['total']['total']
    goals_favor_average = response['response']['goals']['for']['average']['total']

    goals_against = response['response']['goals']['against']['total']['total']
    goals_against_average = response['response']['goals']['against']['average']['total']
    clean_sheet = response['response']['clean_sheet']['total']
    failed_to_score = response['response']['failed_to_score']['total']
    penalty = response['response']['penalty']['scored']['total']
    penalty_acurracy = response['response']['penalty']['scored']['percentage']

    lista_yellow = list(response['response']['cards']['yellow'].keys())
    
    
    for x in lista_yellow[:-2]:
        if response['response']['cards']['yellow'][x]['total'] is not None:
            contador_yellow = contador_yellow +  int(response['response']['cards']['yellow'][x]['total'])

    lista_red = list(response['response']['cards']['red'].keys())

    
    for x in lista_red[:-2]:
        if response['response']['cards']['red'][x]['total'] is not None:
            contador_red = contador_red +  int(response['response']['cards']['red'][x]['total'])
    
    tupla = (id_league,name_league,season_league,id_team,name_team,match_played,wins_played,draws_played,loses_played,goals_favor,goals_favor_average,goals_against,
            goals_against_average,clean_sheet,failed_to_score,penalty,penalty_acurracy,contador_yellow,contador_red)
    return   tupla 


def league_season_team_player(team,season,league):

    
    page = list(range(1,3))
    
    tupla_accu = []
    for x in page: 
       
       
        url = "https://api-football-v1.p.rapidapi.com/v3/players"
        querystring = {"team":team,"season":season,"league":league, "page":x}
        response = requests.request("GET", url, headers=headers, params=querystring)
        response = response.json()
        
        for x in range(len(response['response'])):
            id_player = response['response'][x]['player']['id']
            id_name = response['response'][x]['player']['name']
            first_name = response['response'][x]['player']['firstname']
            last_name = response['response'][x]['player']['lastname']
            age = response['response'][x]['player']['age']
            height = response['response'][x]['player']['height']
            weight = response['response'][x]['player']['weight']
            appearence = response['response'][x]['statistics'][0]['games']['appearences']
            lineup = response['response'][x]['statistics'][0]['games']['lineups']
            minutes = response['response'][x]['statistics'][0]['games']['minutes']
            position = response['response'][x]['statistics'][0]['games']['position']
            rating = response['response'][x]['statistics'][0]['games']['rating']
            shots_total = response['response'][x]['statistics'][0]['shots']['total']
            shots_on = response['response'][x]['statistics'][0]['shots']['on']
            goles = response['response'][x]['statistics'][0]['goals']['total']
            goles_conceded = response['response'][x]['statistics'][0]['goals']['conceded']
            goles_assists = response['response'][x]['statistics'][0]['goals']['assists']
            goles_saves = response['response'][x]['statistics'][0]['goals']['saves']
            passes_total = response['response'][x]['statistics'][0]['passes']['total']
            passes_key = response['response'][x]['statistics'][0]['passes']['key']
            passes_accuracy = response['response'][x]['statistics'][0]['passes']['accuracy']
            tackles_total = response['response'][x]['statistics'][0]['tackles']['total']
            tackles_blocks = response['response'][x]['statistics'][0]['tackles']['blocks']
            tackles_interceptions = response['response'][x]['statistics'][0]['tackles']['interceptions']
            duels_total = response['response'][x]['statistics'][0]['duels']['total']
            duels_wom = response['response'][x]['statistics'][0]['duels']['won']
            dribbles_total = response['response'][x]['statistics'][0]['dribbles']['attempts']
            dribbles_success = response['response'][x]['statistics'][0]['dribbles']['success']
            fouls_drawn = response['response'][x]['statistics'][0]['fouls']['drawn']
            fouls_committed = response['response'][x]['statistics'][0]['fouls']['committed']
            card_yellow = response['response'][x]['statistics'][0]['cards']['yellow']
            card_red = response['response'][x]['statistics'][0]['cards']['red']
            penalty_won = response['response'][x]['statistics'][0]['penalty']['won']
            penalty_commited = response['response'][x]['statistics'][0]['penalty']['commited']
            penalty_scored = response['response'][x]['statistics'][0]['penalty']['scored']
            penalty_missed = response['response'][x]['statistics'][0]['penalty']['missed']
            penalty_saved = response['response'][x]['statistics'][0]['penalty']['saved']

            tupla = (season,league,team,id_player,id_name,first_name,last_name,age,height,weight,appearence,lineup,
            minutes,position,rating,shots_total,shots_on,goles,goles_conceded,goles_assists,
            goles_saves,passes_total,passes_key,passes_accuracy,tackles_total,
            tackles_blocks,tackles_interceptions,duels_total,duels_wom,dribbles_total,dribbles_success,
            fouls_drawn,fouls_committed,card_yellow,card_red,penalty_won,penalty_commited,penalty_scored,
            penalty_missed,penalty_saved)

            tupla_accu.append(tupla)
    
    return   tupla_accu 


def league_season_team_estadisticas(liga,season):

    df = league_season(liga,season).reset_index().drop(columns = ['index'])
    lista_season_team = []
   
    for x in range(len(df)):
       tupla = league_season_team(df.iloc[x,3],df.iloc[x,4],df.iloc[x,0])
       lista_season_team.append(tupla)

    df_teams = pd.DataFrame(lista_season_team, 
          columns = ['id_league','name_league','season_league','id_team','name_team','match_played','wins_played',
          'draws_played','loses_played','goals_favor','goals_favor_average','goals_against','goals_against_average','clean_sheet',
          'failed_to_score','penalty','penalty_acurracy','contador_yellow','contador_red'])

    df_teams = df_teams.reset_index().drop(columns = ['index'])
    df_teams['goals_favor_average'] = df_teams['goals_favor_average'].apply(lambda x: float(x))
    df_teams['goals_against_average'] = df_teams['goals_against_average'].apply(lambda x: float(x))
    df_teams['penalty_acurracy'] = df_teams['penalty_acurracy'].apply(lambda x : float(x.split('%')[0]))
    return df_teams



def league_season_team_players_estadisticas(liga,season):

    df_teams_players = pd.DataFrame()
    
    df_teams = league_season_team_estadisticas(liga,season)

    for x in range(len(df_teams)):
        df_teams_players_id = pd.DataFrame(league_season_team_player(df_teams.iloc[x,3],df_teams.iloc[x,2],df_teams.iloc[x,0]),
               columns =['season','league','team','id_player','id_name','first_name','last_name','age','height','weight','appearence',
               'lineup','minutes','position','rating','shots_total','shots_on','goles','goles_conceded','goles_assists',
               'goles_saves','passes_total','passes_key','passes_accuracy','tackles_total','tackles_blocks','tackles_interceptions',
               'duels_total','duels_wom','dribbles_total','dribbles_success','fouls_drawn','fouls_committed','card_yellow','card_red',
               'penalty_won','penalty_commited','penalty_scored','penalty_missed','penalty_saved'])
        df_teams_players  = pd.concat([df_teams_players,df_teams_players_id], axis = 0)
    
    df_teams_players['height'] = df_teams_players['height'].fillna('0 cm')
    df_teams_players['height'] = df_teams_players['height'].apply(lambda x : float(x.split(' ')[0]))   
    df_teams_players['weight'] = df_teams_players['weight'].fillna('0 kg')
    df_teams_players['weight'] = df_teams_players['weight'].apply(lambda x : float(x.split(' ')[0]))
    df_teams_players['rating'] = df_teams_players['rating'].fillna(0)
    df_teams_players['rating'] = df_teams_players['rating'].apply(lambda x: float(x))
    df_teams_players['penalty_won'] = df_teams_players['penalty_won'].fillna(0)
    df_teams_players['penalty_commited'] = df_teams_players['penalty_commited'].fillna(0)
    df_teams_players = df_teams_players.fillna(0)
    
    #df_teams_players = df_teams_players.rename(columns = {'team':'id_team'})
    #df_teams = df_teams[['id_team','name_team']]    
    #df_teams_players = pd.merge(df_teams_players,df_teams, how ='left', on =['id_team'])

    df_teams_players = df_teams_players.reset_index().drop(columns = ['index'])

    return df_teams_players





