import pandas as pd
import altair as alt
import pandas as pd
import streamlit as st
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from st_aggrid import AgGrid
from st_aggrid.shared import JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd
import plotly.express as px
import functools
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
import pandas as pd
from st_aggrid import AgGrid
from raceplotly.plots import barplot
from collections import deque
import random
import matplotlib as plt

##### DATOS ################################

df_total_equipo = pd.read_csv('LigaChilena_Equipos.csv',sep =';')
df_total_jugador = pd.read_csv('LigaChilena_Jugadores.csv',sep =';')
df_fixture = pd.read_csv('TablaFixtureSeason.csv',sep =';')
#df_total_equipo = df_total_equipo.iloc[:,3:]
#df_total_jugador = df_total_jugador.iloc[:,3:]

def name_to_color(names, r_min=0, r_max=255, g_min=0, g_max=255, b_min=0, b_max=255):
    """Mapping of names to random rgb colors.
    Parameters:
    df (Series): Pandas Series containing names.
    r_min (int): Mininum intensity of the red channel (default 0).
    r_max (int): Maximum intensity of the red channel (default 255).
    g_min (int): Mininum intensity of the green channel (default 0).
    g_max (int): Maximum intensity of the green channel (default 255).
    b_min (int): Mininum intensity of the blue channel (default 0).
    b_max (int): Maximum intensity of the blue channel (default 255).
    Returns:
    dictionary: Mapping of names (keys) to random rgb colors (values)
    """
    mapping_colors = dict()
    
    for name in names.unique():
        red = random.randint(r_min, r_max)
        green = random.randint(g_min, g_max)
        blue = random.randint(b_min, b_max)
        rgb_string = 'rgb({}, {}, {})'.format(red, green, blue)
    
        mapping_colors[name] = rgb_string
    
    return mapping_colors


mapping_colors_man = name_to_color(df_fixture['Equipos'], 0, 185, 0, 185, 125, 255)


##### ALTAIR ##############################

st.set_page_config(page_title='SWAST - Handover Delays',  layout='wide', page_icon=':ambulance:')

#this is the header


t1, t2 = st.columns((0.07,1)) 

t1.image('logocampeonato.png', width =75)
t2.title("Estadistica del Campeonato Nacional Plan Vital")
t2.markdown(" **by:** Francisco Macaya  **| email:** francisco.macaya22@gmail.com")


with st.spinner('Updating Report...'):
    
    #Metrics setting and rendering
    
    periodo_select = st.selectbox('Elige la Temporada', np.sort(df_total_equipo['Periodo'].unique())[::-1], help = 'Filtro para Elegir la temporada')
    

    if int(periodo_select) == 2022:
        height = 550
        limit = '14'
    elif int(periodo_select) == 2021:
        height = 570
        limit = '15'
    else:
        height = 600
        limit = '16'


    t1, t2 = st.columns((1,1)) 

    with t1:
       df_total_equipo_per = df_total_equipo.loc[df_total_equipo['Periodo'] == int(periodo_select)]
       df_total_jugador_per = df_total_jugador.loc[df_total_jugador['Periodo'] == int(periodo_select)]
       df_total_jugador_per = df_total_jugador_per.rename({'name':'Equipo'},axis = 1)
       df_total_equipo_per = df_total_equipo_per.sort_values(by = 'Puntos',ascending = False)
       df_total_equipo_per = df_total_equipo_per[['name_team','match_played','wins_played','draws_played','loses_played','Puntos']]
       df_total_equipo_per = df_total_equipo_per.rename({'name_team':'Equipo','match_played':'PJ','wins_played':'V','draws_played':'E','loses_played':'P','Puntos':'Puntaje'},axis = 1)
       
       
       df_total_equipo_per = df_total_equipo_per.reset_index().drop(columns =['index'])
       df_total_equipo_per = df_total_equipo_per.reset_index()
       df_total_equipo_per = df_total_equipo_per.rename({'index':'Rank'}, axis = 1 )
       
       df_total_equipo_per['Rank'] = df_total_equipo_per['Rank'] +1
       gb = GridOptionsBuilder.from_dataframe(df_total_equipo_per)

       
       if limit =='14':
            cellsytle_jscode = JsCode("""
    function(params) {
        if (params.value < 3)  {
            return {
                'color': 'white',
                'backgroundColor': 'crimson'
            }
        } else if (params.value < 8) {
            return {
                'color': 'white',
                'backgroundColor': 'darkblue'
            }
        } else if (params.value < 14) {
            return {
                'color': 'black',
                'backgroundColor': 'white'
            }
        } else if (params.value > 14) {
            return {
                'color': 'white',
                'backgroundColor': 'gray'
            }
        }   
    };
    """)


       elif limit =='15':
            cellsytle_jscode = JsCode("""
    function(params) {
        if (params.value < 3)  {
            return {
                'color': 'white',
                'backgroundColor': 'crimson'
            }
        } else if (params.value < 8) {
            return {
                'color': 'white',
                'backgroundColor': 'darkblue'
            }
        } else if (params.value < 14) {
            return {
                'color': 'black',
                'backgroundColor': 'white'
            }
        } else if (params.value > 15) {
            return {
                'color': 'white',
                'backgroundColor': 'gray'
            }
        }   
    };
    """)


       else:
            cellsytle_jscode = JsCode("""
    function(params) {
        if (params.value < 3)  {
            return {
                'color': 'white',
                'backgroundColor': 'crimson'
            }
        } else if (params.value < 8) {
            return {
                'color': 'white',
                'backgroundColor': 'darkblue'
            }
        } else if (params.value < 14) {
            return {
                'color': 'black',
                'backgroundColor': 'white'
            }
        } else if (params.value > 14) {
            return {
                'color': 'white',
                'backgroundColor': 'gray'
            }
        }   
    };
    """)



       gb.configure_columns(
        (
            "Rank"),cellStyle=cellsytle_jscode   )
       gb.configure_pagination()
       gb.configure_columns(("account_name", "symbol"), pinned=True)
       gridOptions = gb.build()
       AgGrid(df_total_equipo_per, gridOptions=gridOptions, allow_unsafe_jscode=True, height = height)
 

       original_title = '<p style="color:crimson; font-weight: bold; font-size: 10px;">Nota 1: Clasificados a la Copa Libertadores</p>'
       st.markdown(original_title, unsafe_allow_html=True)
    
       original_title = '<p style="color:darkblue; font-weight: bold; font-size: 10px;">Nota 2: Clasificados a la Copa Sudamericana</p>'
       st.markdown(original_title, unsafe_allow_html=True)

       original_title = '<p style="color:gray; font-weight: bold; font-size: 10px;">Nota 3: Descendiendo de Categoria</p>'
       st.markdown(original_title, unsafe_allow_html=True)

    with t2:

        

        st.subheader("Evolución de los Top Five equipos",)
        df_fixture['Puntos'] = df_fixture['Puntos'].astype(int)
        df_fixture = df_fixture.loc[df_fixture['season'] == int(periodo_select)]

        mapping_colors_man['Colo Colo'] = 'rgba(255,255,255)'
        #mapping_colors_man['Nublense'] = 'rgba(240,0,0)'
        #mapping_colors_man['Curico Unido'] = 'rgba(220,20,60)'
        #mapping_colors_man['Cobresal'] = 'rgba(255,97,3)'
        #mapping_colors_man['Palestino'] = 'rgba(61,145,64)'

        print(mapping_colors_man['Nublense'])

        df_fixture['color'] = df_fixture['Equipos'].map(mapping_colors_man)
        df_fixture['Puntos'] = df_fixture['Puntos'].apply(lambda x : int(x))
        raceplot = barplot(df_fixture,  item_column='Equipos', value_column='Puntos', time_column='fixture',top_entries=5, item_color=mapping_colors_man)
        #raceplot.bar_label(barplot, fmt='%.2f')
        fig=raceplot.plot(item_label = 'Equipos', value_label = 'Puntaje', time_label = 'Fecha :', frame_duration = 2000)
        st.plotly_chart(fig, use_container_width=True)

    st.header("¿Quienes son los mejores?",)


    st.write("""**Nota:** Los puntajes por cada posición se obtuvieron mediante ponderaciones segun la posiciones del jugador, utilizando las siguientes metricas por partido:
        disparos al arco, goles, asistencias, pases claves,precisión de pases,tackles bloqueados y interceptados,foul cometidos,tarjetas amarillas, tarjetas rojas, penales ganados,
        penales convertidos, penales perdidos, penales salvados,duelos ganados, dribbles exitosos, apariciones, edad y estatura.""")
    


    col1, col2 = st.columns((1,1))

    with col1:
        ## Atacantes 

        posicion_select = st.selectbox('¿Cual es la posición a elegir?', np.sort(df_total_jugador_per['position'].unique()), help = 'Filtro para Elegir la temporada')


        chart = functools.partial(st.plotly_chart)
        df_total_jugador_per_attack = df_total_jugador_per.loc[df_total_jugador_per['position'] ==posicion_select]
    
        df_total_jugador_per_attack['rank'] = df_total_jugador_per_attack['rank'].apply(lambda x : round(x,0)) 
        df_total_jugador_per_attack = df_total_jugador_per_attack.sort_values(by ='rank',ascending=False)[:5]

        fig = px.bar(df_total_jugador_per_attack, x = 'id_name', y='rank',text='rank')
        #fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    
        #fig.update_layout(legend=dict(x =1, y =1, font=dict(size= 8)))

        fig.update_traces(marker_color='crimson')
        fig.update_layout(showlegend=True, plot_bgcolor='white')

        fig.update_layout(title_text="Top 5 Mejores {}".format(posicion_select),title_x=0,margin= dict(l=0,r=10,b=20,t=50), yaxis_title='Puntajes', xaxis_title='Jugadores')
        chart(fig)

    with col2:
        


        if posicion_select == 'Attacker':

            df_total_jugador_per_attack = df_total_jugador_per.loc[df_total_jugador_per['position'] ==posicion_select]
            df_total_jugador_per_attack['rank'] = df_total_jugador_per_attack['rank'].apply(lambda x : round(x,2)) 
            df_total_jugador_per_attack = df_total_jugador_per_attack.sort_values(by ='rank',ascending=False)[:5]
            posicion_select = st.selectbox('¿Que jugador quieres revisar?', np.sort(df_total_jugador_per_attack['id_name'].unique()), help = 'Filtro para Elegir la temporada')
            df_total_jugador_per_attack = df_total_jugador_per_attack.loc[df_total_jugador_per_attack['id_name'] == posicion_select]

            ## Caracteristicas

            df_total_jugador_per_attack['goles_app'] = round(df_total_jugador_per_attack['goles_app']*100,0)
            df_total_jugador_per_attack['goles_assistes_app'] = round(df_total_jugador_per_attack['goles_assistes_app']*100,0)
            df_total_jugador_per_attack['shot_on_app'] = round(df_total_jugador_per_attack['shot_on_app']*100,0)
            df_total_jugador_per_attack['penalty_scored_app'] = round(df_total_jugador_per_attack['penalty_scored_app']*100,0)
            df_total_jugador_per_attack['duels_wom_app'] = round(df_total_jugador_per_attack['duels_wom_app']*100,0)
            df_total_jugador_per_attack['dribbles_success_app'] = round(df_total_jugador_per_attack['dribbles_success_app']*100,0)
         #   df_total_jugador_per_attack['lineup_app'] = round(df_total_jugador_per_attack['lineup_app']*100,0)


            df_total_jugador_per_attack = pd.melt(df_total_jugador_per_attack[['id_name','goles_app','goles_assistes_app','shot_on_app','penalty_scored_app','duels_wom_app','dribbles_success_app']], id_vars=["id_name"], 
                  var_name="Skills", value_name="Value")

            fig = go.Figure(data=go.Scatterpolar(
            r=df_total_jugador_per_attack['Value'].values,
            theta=df_total_jugador_per_attack['Skills'].values,
            fill='toself',
            line=dict(color='crimson',
                        width=5)))

            fig.update_layout(
            polar=dict(
            radialaxis=dict(
            visible=True),),
            showlegend=False)

            fig.update_layout({
            'plot_bgcolor': 'rgba(255, 255, 255)',
            'paper_bgcolor': 'rgba(255, 255, 255)',})

            st.write(fig)


        if posicion_select == 'Defender':

            df_total_jugador_per_attack = df_total_jugador_per.loc[df_total_jugador_per['position'] ==posicion_select]
            df_total_jugador_per_attack['rank'] = df_total_jugador_per_attack['rank'].apply(lambda x : round(x,2)) 
            df_total_jugador_per_attack = df_total_jugador_per_attack.sort_values(by ='rank',ascending=False)[:5]
            posicion_select = st.selectbox('¿Que jugador quieres revisar?', np.sort(df_total_jugador_per_attack['id_name'].unique()), help = 'Filtro para Elegir la temporada')
            df_total_jugador_per_attack = df_total_jugador_per_attack.loc[df_total_jugador_per_attack['id_name'] == posicion_select]

            ## Caracteristicas

            df_total_jugador_per_attack['passes_accuracy'] = round(df_total_jugador_per_attack['passes_accuracy'])
            df_total_jugador_per_attack['tackles_blocks_app'] = round(df_total_jugador_per_attack['tackles_blocks_app']*100,0)
            df_total_jugador_per_attack['tackles_interceptions_app'] = round(df_total_jugador_per_attack['tackles_interceptions_app']*100,0)
            df_total_jugador_per_attack['duels_wom_app'] = round(df_total_jugador_per_attack['duels_wom_app']*100,0)
            df_total_jugador_per_attack['goles_app'] = round(df_total_jugador_per_attack['goles_app']*100,0)
            df_total_jugador_per_attack['passes_key_app'] = round(df_total_jugador_per_attack['passes_key_app']*100,0)
         #   df_total_jugador_per_attack['lineup_app'] = round(df_total_jugador_per_attack['lineup_app']*100,0)


            df_total_jugador_per_attack = pd.melt(df_total_jugador_per_attack[['id_name','passes_accuracy','tackles_blocks_app','tackles_interceptions_app','duels_wom_app','goles_app','passes_key_app']], id_vars=["id_name"], 
                  var_name="Skills", value_name="Value")

            fig = go.Figure(data=go.Scatterpolar(
            r=df_total_jugador_per_attack['Value'].values,
            theta=df_total_jugador_per_attack['Skills'].values,
            fill='toself',
            line=dict(color='crimson',
                        width=5)))

            fig.update_layout(
            polar=dict(
            radialaxis=dict(
            visible=True),),
            showlegend=False)

            fig.update_layout({
            'plot_bgcolor': 'rgba(255, 255, 255)',
            'paper_bgcolor': 'rgba(255, 255, 255)',})

            st.write(fig)

    
        if posicion_select == 'Goalkeeper':

            df_total_jugador_per_attack = df_total_jugador_per.loc[df_total_jugador_per['position'] ==posicion_select]
            df_total_jugador_per_attack['rank'] = df_total_jugador_per_attack['rank'].apply(lambda x : round(x,2)) 
            df_total_jugador_per_attack = df_total_jugador_per_attack.sort_values(by ='rank',ascending=False)[:5]
            posicion_select = st.selectbox('¿Que jugador quieres revisar?', np.sort(df_total_jugador_per_attack['id_name'].unique()), help = 'Filtro para Elegir la temporada')
            df_total_jugador_per_attack = df_total_jugador_per_attack.loc[df_total_jugador_per_attack['id_name'] == posicion_select]

            ## Caracteristicas


            df_total_jugador_per_attack['goles_saves_app'] = round(df_total_jugador_per_attack['goles_saves_app']*100,0)
            df_total_jugador_per_attack['goles_conceded_app'] = 1- round(df_total_jugador_per_attack['goles_conceded_app']*100,0)
            df_total_jugador_per_attack['passes_accuracy'] = round(df_total_jugador_per_attack['passes_accuracy'],0)
            df_total_jugador_per_attack['penalty_saved_app'] = round(df_total_jugador_per_attack['penalty_saved_app']*100,0)
         #   df_total_jugador_per_attack['lineup_app'] = round(df_total_jugador_per_attack['lineup_app']*100,0)


            df_total_jugador_per_attack = pd.melt(df_total_jugador_per_attack[['id_name','goles_saves_app','goles_conceded_app','passes_accuracy','penalty_saved_app']], id_vars=["id_name"], 
                  var_name="Skills", value_name="Value")

            fig = go.Figure(data=go.Scatterpolar(
            r=df_total_jugador_per_attack['Value'].values,
            theta=df_total_jugador_per_attack['Skills'].values,
            fill='toself',
            line=dict(color='crimson',
                        width=5)))

            fig.update_layout(
            polar=dict(
            radialaxis=dict(
            visible=True),),
            showlegend=False)

            fig.update_layout({
            'plot_bgcolor': 'rgba(255, 255, 255)',
            'paper_bgcolor': 'rgba(255, 255, 255)',})

            st.write(fig)

        if posicion_select == 'Midfielder':

            df_total_jugador_per_attack = df_total_jugador_per.loc[df_total_jugador_per['position'] ==posicion_select]
            df_total_jugador_per_attack['rank'] = df_total_jugador_per_attack['rank'].apply(lambda x : round(x,2)) 
            df_total_jugador_per_attack = df_total_jugador_per_attack.sort_values(by ='rank',ascending=False)[:5]
            posicion_select = st.selectbox('¿Que jugador quieres revisar?', np.sort(df_total_jugador_per_attack['id_name'].unique()), help = 'Filtro para Elegir la temporada')
            df_total_jugador_per_attack = df_total_jugador_per_attack.loc[df_total_jugador_per_attack['id_name'] == posicion_select]

            ## Caracteristicas


            df_total_jugador_per_attack['goles_app'] = round(df_total_jugador_per_attack['goles_app']*100,0)
            df_total_jugador_per_attack['goles_assistes_app'] = 1- round(df_total_jugador_per_attack['goles_assistes_app']*100,0)
            df_total_jugador_per_attack['passes_accuracy'] = round(df_total_jugador_per_attack['passes_accuracy'],0)
            df_total_jugador_per_attack['tackles_blocks_app'] = round(df_total_jugador_per_attack['tackles_blocks_app']*100,0)
            df_total_jugador_per_attack['tackles_interceptions_app'] = round(df_total_jugador_per_attack['tackles_interceptions_app']*100,0)
            df_total_jugador_per_attack['shot_on_app'] = round(df_total_jugador_per_attack['shot_on_app']*100,0)
            df_total_jugador_per_attack['duels_wom_app'] = round(df_total_jugador_per_attack['duels_wom_app']*100,0)
            df_total_jugador_per_attack['dribbles_success_app'] = round(df_total_jugador_per_attack['dribbles_success_app']*100,0)

         #   df_total_jugador_per_attack['lineup_app'] = round(df_total_jugador_per_attack['lineup_app']*100,0)


            df_total_jugador_per_attack = pd.melt(df_total_jugador_per_attack[['id_name','goles_app','goles_assistes_app','passes_accuracy','tackles_blocks_app','tackles_interceptions_app','shot_on_app','duels_wom_app','dribbles_success_app']], id_vars=["id_name"], 
                  var_name="Skills", value_name="Value")

            fig = go.Figure(data=go.Scatterpolar(
            r=df_total_jugador_per_attack['Value'].values,
            theta=df_total_jugador_per_attack['Skills'].values,
            fill='toself',
            line=dict(color='crimson',
                        width=5)))

            fig.update_layout(
            polar=dict(
            radialaxis=dict(
            visible=True),),
            showlegend=False)

            fig.update_layout({
            'plot_bgcolor': 'rgba(255, 255, 255)',
            'paper_bgcolor': 'rgba(255, 255, 255)',})

            st.write(fig)