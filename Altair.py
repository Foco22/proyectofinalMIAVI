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

##### DATOS ################################

df_total_equipo = pd.read_csv('LigaChilena_Equipos.csv',sep =';')
df_total_jugador = pd.read_csv('LigaChilena_Jugadores.csv',sep =';')
#df_total_equipo = df_total_equipo.iloc[:,3:]
#df_total_jugador = df_total_jugador.iloc[:,3:]


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
 
    df_total_equipo_per = df_total_equipo.loc[df_total_equipo['Periodo'] == int(periodo_select)]
    df_total_jugador_per = df_total_jugador.loc[df_total_jugador['Periodo'] == int(periodo_select)]
    

    df_total_jugador_per = df_total_jugador_per.rename({'name':'Equipo'},axis = 1)

    df_total_equipo_per = df_total_equipo_per.sort_values(by = 'Puntos',ascending = False)

    df_total_equipo_per = df_total_equipo_per[['Periodo','name_team','match_played','wins_played','draws_played','loses_played','goals_favor','goals_against','penalty','Puntos']]
    
    df_total_equipo_per = df_total_equipo_per.rename({'name_team':'Equipo','match_played':'PJ','wins_played':'V','draws_played':'E','loses_played':'P','goals_favor':'GA','goals_against':'GE','penalty':'Penales','Puntos':'Puntaje'},axis = 1)
    gb = GridOptionsBuilder.from_dataframe(df_total_equipo_per)
    gb.configure_columns(
        (
            "last_price_change",
            "total_gain_loss_dollar",
            "total_gain_loss_percent",
            "today's_gain_loss_dollar",
            "today's_gain_loss_percent",
        )   )
    gb.configure_pagination()
    gb.configure_columns(("account_name", "symbol"), pinned=True)
    gridOptions = gb.build()

    AgGrid(df_total_equipo_per, gridOptions=gridOptions, allow_unsafe_jscode=True)

    

    st.header("¿Quienes son los mejores?",)


    st.write("""**Nota:** Los puntajes por cada posición se obtuvieron mediante ponderaciones segun la posiciones del jugador, utilizando las siguientes metricas por partido:
        disparos al arco, goles, asistencias, pases claves,precisión de pases,tackles bloqueados y interceptados,foul cometidos,tarjetas amarillas, tarjetas rojas, penales ganados,
        penales convertidos, penales perdidos, penales salvados,duelos ganados, dribbles exitosos, apariciones, edad y estatura.""")
    
    col1, col2 = st.columns((1,1))

    with col1:
        ## Atacantes 


        chart = functools.partial(st.plotly_chart)
        df_total_jugador_per_attack = df_total_jugador_per.loc[df_total_jugador_per['position'] =='Attacker']
    
        df_total_jugador_per_attack['rank'] = df_total_jugador_per_attack['rank'].apply(lambda x : round(x,2)) 
        df_total_jugador_per_attack = df_total_jugador_per_attack.sort_values(by ='rank',ascending=False)[:5]

        fig = px.bar(df_total_jugador_per_attack, x = 'id_name', y='rank',text='rank', color = 'Equipo')
        #fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    
        #fig.update_layout(legend=dict(x =1, y =1, font=dict(size= 8)))

        #fig.update_traces(marker_color='crimson')
        fig.update_layout(showlegend=True, plot_bgcolor='white')

        fig.update_layout(title_text="Top 5 Mejores Delanteros",title_x=0,margin= dict(l=0,r=10,b=20,t=50), yaxis_title='Puntajes', xaxis_title='Jugadores')
        chart(fig)
    
    with col2:
        
        ## Mediocampistas 

        chart = functools.partial(st.plotly_chart)
        df_total_jugador_per_attack = df_total_jugador_per.loc[df_total_jugador_per['position'] =='Midfielder']
    
        df_total_jugador_per_attack['rank'] = df_total_jugador_per_attack['rank'].apply(lambda x : round(x,2)) 
        df_total_jugador_per_attack = df_total_jugador_per_attack.sort_values(by ='rank',ascending=False)[:5]

        fig = px.bar(df_total_jugador_per_attack, x = 'id_name', y='rank',text='rank', color = 'Equipo')
        #fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    
        #fig.update_traces(marker_color='crimson')
        fig.update_layout(showlegend=True, plot_bgcolor='white')
        fig.update_layout(title_text="Top 5 Mejores Mediocampistas",title_x=0,margin= dict(l=0,r=10,b=20,t=50), yaxis_title='Puntajes', xaxis_title='Jugadores')
        chart(fig)


    col1, col2 = st.columns((1,1))

    with col1:
        
        ## Mediocampistas 

        chart = functools.partial(st.plotly_chart)
        df_total_jugador_per_attack = df_total_jugador_per.loc[df_total_jugador_per['position'] =='Defender']
    
        df_total_jugador_per_attack['rank'] = df_total_jugador_per_attack['rank'].apply(lambda x : round(x,2)) 
        df_total_jugador_per_attack = df_total_jugador_per_attack.sort_values(by ='rank',ascending=False)[:5]

        fig = px.bar(df_total_jugador_per_attack, x = 'id_name', y='rank',text='rank', color = 'Equipo')
        #fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    
        #fig.update_traces(marker_color='crimson')
        fig.update_layout(showlegend=True, plot_bgcolor='white')
        fig.update_layout(title_text="Top 5 Mejores Defensas",title_x=0,margin= dict(l=0,r=10,b=20,t=50), yaxis_title='Puntajes', xaxis_title='Jugadores')
        chart(fig)


    with col2:
        
        ## Mediocampistas 

        chart = functools.partial(st.plotly_chart)

        df_total_jugador_per_attack = df_total_jugador_per.loc[df_total_jugador_per['position'] =='Goalkeeper']
    
        df_total_jugador_per_attack['rank'] = df_total_jugador_per_attack['rank'].apply(lambda x : round(x,2)) 
        df_total_jugador_per_attack = df_total_jugador_per_attack.sort_values(by ='rank',ascending=False)[:5]
        
        fig = px.bar(df_total_jugador_per_attack, x = 'id_name', y='rank',text='rank', color = 'Equipo')
        #fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    
        #fig.update_traces(marker_color='crimson')
        fig.update_layout(showlegend=True, plot_bgcolor='white')
        fig.update_layout(title_text="Top 5 Mejores Arqueros",title_x=0,margin= dict(l=0,r=10,b=20,t=50), yaxis_title='Puntajes', xaxis_title='Jugadores')
        chart(fig)
