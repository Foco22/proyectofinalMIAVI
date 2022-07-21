from turtle import Turtle
import requests 
import pandas as pd
import ExtraccionDatosApi as extraccion
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

################ Parametros ##################################


################ Main ########################################


def get_extraccion(sesiones):

    ## Futbol Chileno Liga 265 

    df_total_equipo_liga = pd.DataFrame()
    df_total_jugador_chilena_equipos = pd.DataFrame()    

    for x in sesiones:
        
        print('Periodo : {}'.format(x))
        equipo_liga = extraccion.league_season(265,[x])
        liga_chilena_equipos = extraccion.league_season_team_estadisticas(265,[x])
        jugador_chilena_equipos = extraccion.league_season_team_players_estadisticas(265,[x])
    
        equipo_liga = equipo_liga.rename(columns = {'id':'team'})
        jugador_chilena_equipos = pd.merge(jugador_chilena_equipos,equipo_liga[['team','name']], on = 'team', how = 'left')
        
        liga_chilena_equipos['Periodo'] = x
        jugador_chilena_equipos['Periodo'] = x

        df_total_equipo_liga = pd.concat([df_total_equipo_liga,liga_chilena_equipos],axis = 0)
        df_total_jugador_chilena_equipos = pd.concat([df_total_jugador_chilena_equipos,jugador_chilena_equipos],axis = 0)
        #liga_chilena_equipos.to_csv('Equipo_Estadisticas.csv',sep =';')
        #jugador_chilena_equipos.to_csv('Equipo_jugadores_Estadisticas.csv',sep =';')
    
    df_total_equipo_liga.to_csv('LigaChilena_Equipos.csv',sep =';')
    df_total_jugador_chilena_equipos.to_csv('LigaChilena_Jugadores.csv',sep =';')
    
    return df_total_equipo_liga,df_total_jugador_chilena_equipos

####################### Extraccion ############################


#df_total_equipo, df_total_jugador = get_extraccion([2020,2021,2022]


###################### Preprocesamiento #######################

def procesamiento(df_total_jugador,df_total_equipo):
    
    #df_total_equipo, df_total_jugador = get_extraccion([2020,2021,2022])
    
    df_total_jugador['appearence'] = df_total_jugador.apply(lambda row: 32 if row['Periodo'] != 2022 else 16, axis = 1  )
    df_total_jugador['goles'] = df_total_jugador['goles'] + df_total_jugador['penalty_scored']
    
    df_total_jugador['shot_on_app'] = df_total_jugador.apply(lambda row: 0 if row['appearence'] == 0 else row['shots_on']/row['appearence'], axis = 1)
    df_total_jugador['goles_assistes_app'] = df_total_jugador.apply(lambda row: 0 if row['appearence'] == 0 else row['goles_assists']/row['appearence'], axis = 1)
    df_total_jugador['goles_app'] = df_total_jugador.apply(lambda row: 0 if row['appearence'] == 0 else row['goles']/row['appearence'], axis = 1)
    df_total_jugador['goles_saves_app'] = df_total_jugador.apply(lambda row: 0 if row['appearence'] == 0 else row['goles_saves']/row['appearence'], axis = 1)
    df_total_jugador['passes_key_app'] = df_total_jugador.apply(lambda row: 0 if row['appearence'] == 0 else row['passes_key']/row['appearence'], axis = 1)
    df_total_jugador['tackles_blocks_app'] = df_total_jugador.apply(lambda row: 0 if row['appearence'] == 0 else row['tackles_blocks']/row['appearence'], axis = 1)
    df_total_jugador['tackles_interceptions_app'] = df_total_jugador.apply(lambda row: 0 if row['appearence'] == 0 else row['tackles_interceptions']/row['appearence'], axis = 1)
    df_total_jugador['fouls_committed_app'] = df_total_jugador.apply(lambda row: 0 if row['appearence'] == 0 else row['fouls_committed']/row['appearence'], axis = 1)
    df_total_jugador['card_yellow_app'] = df_total_jugador.apply(lambda row: 0 if row['appearence'] == 0 else row['card_yellow']/row['appearence'], axis = 1)
    df_total_jugador['card_red_app'] = df_total_jugador.apply(lambda row: 0 if row['appearence'] == 0 else row['card_red']/row['appearence'], axis = 1)
    df_total_jugador['penalty_won_app'] = df_total_jugador.apply(lambda row: 0 if row['appearence'] == 0 else row['penalty_won']/row['appearence'], axis = 1)
    df_total_jugador['penalty_commited_app'] = df_total_jugador.apply(lambda row: 0 if row['appearence'] == 0 else row['penalty_commited']/row['appearence'], axis = 1)
    df_total_jugador['penalty_scored_app'] = df_total_jugador.apply(lambda row: 0 if row['appearence'] == 0 else row['penalty_scored']/row['appearence'], axis = 1)
    df_total_jugador['penalty_missed_app'] = df_total_jugador.apply(lambda row: 0 if row['appearence'] == 0 else row['penalty_missed']/row['appearence'], axis = 1)
    df_total_jugador['penalty_saved_app'] = df_total_jugador.apply(lambda row: 0 if row['appearence'] == 0 else row['penalty_saved']/row['appearence'], axis = 1)
    df_total_jugador['duels_wom_app'] = df_total_jugador.apply(lambda row: 0 if row['appearence'] == 0 else row['duels_wom']/row['appearence'], axis = 1)
    df_total_jugador['dribbles_success_app'] = df_total_jugador.apply(lambda row: 0 if row['appearence'] == 0 else row['dribbles_success']/row['appearence'], axis = 1)
    df_total_jugador['lineup_app'] = df_total_jugador.apply(lambda row: 0 if row['appearence'] == 0 else row['lineup']/row['appearence'], axis = 1)
    df_total_jugador['goles_conceded_app'] = df_total_jugador.apply(lambda row: 0 if row['appearence'] == 0 else row['goles_conceded']/row['appearence'], axis = 1)
    df_total_jugador['age_n'] = (df_total_jugador['age']) #Max 42
    df_total_jugador['height_r'] = df_total_jugador['height']/200 #Max 200
    df_total_jugador['passes_accuracy_r'] = df_total_jugador['passes_accuracy']/100
    df_total_jugador = df_total_jugador.fillna(0)

    #Scalar datos
    scaler = MinMaxScaler()
    scaler = scaler.fit(df_total_jugador.iloc[:,43:])
    scaler_r = scaler.transform(df_total_jugador.iloc[:,43:])
    df_norm_r = pd.DataFrame(scaler_r, columns = df_total_jugador.iloc[:,43:].columns)
    df_total_jugador = pd.concat([df_total_jugador.iloc[:,:43],df_norm_r], axis = 1)
    df_total_jugador['age_n']  = 1-df_total_jugador['age_n'] 

    df_total_jugador['rank'] = 0

    for x in range(df_total_jugador.shape[0]):
    
        if df_total_jugador.iloc[x,14] == 'Attacker':

        # Indicador Attack = 
# 3*shot_on_app + 3*goles_app + 1*goles_assistes_app +  1*passes_key_app + 0* tackles_blocks_app + 1*passes_accuracy + 
# 0*tackles_interceptions_app - 0*fouls_committed_app - 0*card_yellow_app - 1*card_red_app + 
# 1*penalty_won_app + 2*penalty_scored_app - 1*penalty_missed_app + 0*penalty_commited_app +
# penalty_saved_app*0 + 1*duels_wom_app + 3*dribbles_success_app + 3*lineup_app + 3*height_r + 3*age_r 
       
          df_total_jugador.iloc[x,65] = 5*df_total_jugador.iloc[x,43] + 4*df_total_jugador.iloc[x,45] +  1*df_total_jugador.iloc[x,47]
          + 1*df_total_jugador.iloc[x,64] - 1*df_total_jugador.iloc[x,51] +  1*df_total_jugador.iloc[x,53] + 2*df_total_jugador.iloc[x,55]  
          - 1*df_total_jugador.iloc[x,56] + 1*df_total_jugador.iloc[x,58] + 3*df_total_jugador.iloc[x,59]   + 3*df_total_jugador.iloc[x,60]
          + 3*df_total_jugador.iloc[x,63] + 3*df_total_jugador.iloc[x,62]   

        if df_total_jugador.iloc[x,14] == 'Midfielder':

# Indicador Medio = 
# 1*shot_on_app + 1*goles_app + 3*goles_assistes_app +  3*passes_key_app + 3*passes_accuracy + 2* tackles_blocks_app + 
# 2*tackles_interceptions_app - 2*fouls_committed_app - 1*card_yellow_app - 2*card_red_app + 
# 1*penalty_won_app + 1*penalty_scored_app + 0*penalty_missed_app - 2*penalty_commited_app +
# 0*penalty_saved_app + 3*duels_wom_app + 1*dribbles_success_app + 3*lineup_app + 2*height_r + 3*age_r 

       
          df_total_jugador.iloc[x,65] = 1*df_total_jugador.iloc[x,43] + 1*df_total_jugador.iloc[x,45] +  3*df_total_jugador.iloc[x,47]
          + 2*df_total_jugador.iloc[x,48] + 3*df_total_jugador.iloc[x,64] + 2*df_total_jugador.iloc[x,49] +  2*df_total_jugador.iloc[x,50]
          - 1*df_total_jugador.iloc[x,51] - 2*df_total_jugador.iloc[x,52] + 1*df_total_jugador.iloc[x,53] + 1*df_total_jugador.iloc[x,55] 
          - 2*df_total_jugador.iloc[x,54] +  3*df_total_jugador.iloc[x,58] + 2*df_total_jugador.iloc[x,59] + 3*df_total_jugador.iloc[x,60]
          + 3*df_total_jugador.iloc[x,63] + 3*df_total_jugador.iloc[x,62]
       


        if df_total_jugador.iloc[x,14] == 'Defender':

# Indicador Defensa = 
# 1*shot_on_app + 1*goles_app + 1*goles_assistes_app +  1*passes_key_app + 2*passes_accuracy + 3* tackles_blocks_app + 
# 3*tackles_interceptions_app - 2*fouls_committed_app - 1*card_yellow_app - 2*card_red_app + 
# 1*penalty_won_app + 1*penalty_scored_app + 0*penalty_missed_app - 3*penalty_commited_app +
# 0*penalty_saved_app + 3*duels_wom_app + 0*dribbles_success_app + 3*lineup_app + 3*age_r + 3*height_r

       
          df_total_jugador.iloc[x,65] = 1*df_total_jugador.iloc[x,43] + 1*df_total_jugador.iloc[x,45] +  1*df_total_jugador.iloc[x,47] 
          + 2*df_total_jugador.iloc[x,64] +  3*df_total_jugador.iloc[x,48] + 3*df_total_jugador.iloc[x,49] + 2*df_total_jugador.iloc[x,50]
          - 1*df_total_jugador.iloc[x,51] - 2*df_total_jugador.iloc[x,52] + 1*df_total_jugador.iloc[x,53] + 1*df_total_jugador.iloc[x,55] 
          - 3*df_total_jugador.iloc[x,54] + 3*df_total_jugador.iloc[x,58] +3*df_total_jugador.iloc[x,60]
          + 3*df_total_jugador.iloc[x,63] + 3*df_total_jugador.iloc[x,62]


        if df_total_jugador.iloc[x,14] == 'Goalkeeper':


# Indicador Goalkepper = 
# 3*goles_saves_app - 3*goles_conceded_app + 1*passes_accuracy + 1*penalty_saved_app + 3*lineup_app + 3*age_r + 3*height_r

   
          df_total_jugador.iloc[x,65] =  -3*df_total_jugador.iloc[x,61] + 3*df_total_jugador.iloc[x,46] + 1*df_total_jugador.iloc[x,64] 
          + 3*df_total_jugador.iloc[x,60] + 3*df_total_jugador.iloc[x,63] + 3*df_total_jugador.iloc[x,62]


    df_total_equipo['Puntos'] = df_total_equipo['wins_played']*3 + df_total_equipo['draws_played']*1 + df_total_equipo['loses_played']*0
    return df_total_equipo,df_total_jugador




#### ALTIER ##############################################################


