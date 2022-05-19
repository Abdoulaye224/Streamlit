from cProfile import label
from cgitb import text
from contextlib import nullcontext
import datetime
from optparse import Option
from unicodedata import numeric
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

#***********************************************************************************

#Fonction pour des animations 
import json
import requests  # pip install requests
from streamlit_lottie import st_lottie 

#****************************Style**************************
st.markdown("""
<style>
.paragraphe {
    font-size:20px !important;
}
</style>
""", unsafe_allow_html=True)
#************************************************************


def lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

#chargement d'une animation 
lottie_chargement = lottie_url("https://assets4.lottiefiles.com/packages/lf20_w51pcehl.json")
lottie_acceuil = lottie_url("https://assets8.lottiefiles.com/packages/lf20_i2eyukor.json")
lotti_inprogress = lottie_url("https://assets7.lottiefiles.com/packages/lf20_earcnwm3.json")

#************************************************************************************

pages=["Accueil", "Cours boursiers", "indicateurs clés", "Dividende"]
choix=st.sidebar.selectbox("Menu", pages)



#************************************************************************************
data = pd.read_excel(
        io="./projet_streamlit.xlsx",
        engine="openpyxl",
        sheet_name="ENGIY",
        skiprows=0,
        usecols="A:K",
        nrows=62,
    )

data.rename(columns = {'Rentabilité mensuel':'rent_month', 'rentabilité moyenne annuel':'means_rent_year', "Volatilité annuel de l'action":'volatility'}, inplace = True)
data['Date'] = data['Date'].apply(lambda x: x.strftime('%Y-%m-%d')) 
#************************************************************************************

#************************** Fonction pour charger la donnée **************************

def load_data():
    df = pd.read_csv("ENGIY.csv", index_col='Date')


    numeric_df = df.select_dtypes(['float', 'int'])
    numeric_cols = numeric_df.columns

    text_df = df.select_dtypes(['object'])
    text_cols = text_df.columns


    return df, numeric_cols, text_cols

df, numeric_cols, text_cols = load_data()
#*************************************************************************************
if choix=="Accueil":
    st.markdown("<h1 style='text-align: left; color: cadetblue; margin-top:-60px'>ACCUEIL</h1>", unsafe_allow_html=True)
    st.title("Tableau de bord de suivi d'actif ")
    st.markdown('Pour la période de **mai 2017** à **mai 2022**.')
    st_lottie(lottie_acceuil,speed=1,reverse=False,loop=True,quality="low",height=None,width=None,key=None)
    st.markdown("<p class='paragraphe'> Bienvenue sur notre tableau de bord qui a pour objection de suivre l'historique de l'action de la société ENGIE sur la période de mai 2017 à mai 2022 </p>", unsafe_allow_html=True)
    st.markdown('## PARTIE 1 : ')
    st.markdown("<p class='paragraphe'> Dans la première partie vous aurez l'occasion de voir le jeu de données globale pour la période précisée et l'évolution chronologique des différents paramètres </p>", unsafe_allow_html=True)
    st.markdown('## PARTIE 2 : ')
    st.markdown("<p class='paragraphe'> Cette partie consiste à avoir une vue sur l'historique des différentes données high, value, close... de l'entreprise. Vous verrez l'évolution de ces valeurs selon la période </p>", unsafe_allow_html=True)
    st.markdown('## PARTIE 3 : ')
    st.markdown("<p class='paragraphe'> Cette troisième partie permet de faire un Zoom sur certains indicateurs clés tels que la rentabilité annuelle/mensuelle, la volatilité </p>", unsafe_allow_html=True)
    st.markdown('## PARTIE 4 : ')
    st.markdown("<p class='paragraphe'> La quatrième partie vous permettra de voir pendant quelle période l'entreprise engie a versé des dividendes à ses actionnaires ainsi que les valeurs associées </p>", unsafe_allow_html=True)

elif choix=="Cours boursiers":
    st.markdown("<h1 style='text-align: left; color: cadetblue; margin-top:-50px'>Cours boursiers</h1>", unsafe_allow_html=True)
    st.markdown("<p class='paragraphe'> Sur cette page, vous pourrez afficher les données si vous le souhaitez, vous avez aussi la possibilité d'afficher pour chaque colonne l'évolution (vous pourrez combiner plusieurs colonnes également) </p>", unsafe_allow_html=True)

    hide_data = st.checkbox(label="Afficher les données ")

    if hide_data:
        st.write(df)

    st.sidebar.title("Paramètres")

    feature_selection = st.sidebar.multiselect(label="Choix de la valeur", options=numeric_cols)

    df_features = df[feature_selection]

    print('taille', len(feature_selection))

    plotly_figure = px.line(data_frame=df_features, x=df_features.index, y=feature_selection, title="Chronologie")
        
    if len(feature_selection) == 0:
        st.info('Veuillez selectionner la(es) donnée(s) à afficher dans les paramètres ! ')
    else:
        st.plotly_chart(plotly_figure) 


    hide_volum = st.sidebar.checkbox(label="Afficher les volume selon une période ")

    if hide_volum:
        st.subheader('Le volume selon la période souhaitée')

        min_date = datetime.datetime(2017,5,1)
        max_date = datetime.date(2022,4,18)

        a_date = st.date_input("Chosir la période", (min_date, max_date))

        
        tickerSymbol = 'ENGIY'
        tickerData = yf.Ticker(tickerSymbol)

        if len(a_date) == 2:
            start_date = a_date[0].strftime("%Y-%m-%d")
            end_date = a_date[1].strftime("%Y-%m-%d")
            tickerDf = tickerData.history(period='id', start=start_date, end=end_date)
            st.line_chart(tickerDf.Volume)
        else:
            st_lottie(lotti_inprogress,speed=1,reverse=False,loop=True,quality="low",height=200,width=200,key=None,)
elif choix=="indicateurs clés":
    st.markdown("<h1 style='text-align: left; color: cadetblue;'>Indicateurs clés</h1>", unsafe_allow_html=True)
    st.markdown("<p class='paragraphe'> Cette page met en évidence certains indicateurs clés que vous pouvez visualiser en changeant de dates dans l'onglet des paramètres </p>", unsafe_allow_html=True)
    st.info("Les indicateurs 'rentabilité moyenne' et 'volatilité annuelle' ne sont pas possibles à afficher pour toutes les dates possibles. Faudra dans ce cas choisir le premier jour de chaque années pour avoir ces chiffres ou la dernière date présente")


    date_cols = data['Date']

    st.sidebar.title("Paramètres")
    date_selection=st.sidebar.selectbox("Choix date", date_cols)


    data_renta_mens = data[['Date','rent_month']].dropna()
    data_renta_moy_an = data[['Date','means_rent_year']].dropna()
    Volatilite=data[['Date','volatility']].dropna()
    Dividends=data[['Date', 'Dividends']].dropna()
    
    date_month_cols = data_renta_mens['Date']
    date_year_cols = data_renta_moy_an['Date']

    value=data[data['Date']==date_selection]

    if value['means_rent_year'].empty and value['volatility'].empty:
        col1, col2, col3 = st.columns(3)    
        col1.metric("Rentabilité mensuel", value=value['rent_month'], delta_color="inverse")
        col2.metric("rentabilité moyenne annuel", value="mauvaise date...")
        col3.metric("Volatilité annuel de l'action", 'mauvaise date...')
    else:
        col1, col2, col3 = st.columns(3)    
        col1.metric("Rentabilité mensuel", value['rent_month'])
        col2.metric("rentabilité moyenne annuel", value['means_rent_year'])
        col3.metric("Volatilité annuel de l'action", value['volatility'])

elif choix=="Dividende":
    st.markdown("<h1 style='text-align: left; color: cadetblue;'>Dividende</h1>", unsafe_allow_html=True)
    st.info("Cette page vous montre l'ensemble des dividendes versées par action par la société durant les 5 dernières années")
    Dividends=data[['Date', 'Dividends']].dropna()
    div = Dividends['Date']
    date_selection=st.sidebar.selectbox("Choix date", div)

    value=Dividends[Dividends['Date']==date_selection]

    st.markdown("<p class='paragraphe'> Chiffre en € par action <p>", unsafe_allow_html=True)
    st.metric(label=f"Diviende versée à la date du {date_selection}", value=value['Dividends'])





