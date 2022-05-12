from cProfile import label
from cgitb import text
from contextlib import nullcontext
import datetime
from optparse import Option
from turtle import title
from unicodedata import numeric
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from PIL import Image

#***********************************************************************************


#st.title("Tableau de bord de suivi d'actif ")
#st.markdown('Pour la période de **mai 2017** à **mai 2022**.')

pages=["Accueil", "Cours boursiers", "indicateurs clés", "Dividende"]
choix=st.sidebar.selectbox("Menu", pages)

image = Image.open('home.PNG')


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
    st.image(image)

elif choix=="Cours boursiers":
    st.markdown("<h1 style='text-align: left; color: cadetblue; margin-top:-50px'>Cours boursiers</h1>", unsafe_allow_html=True)

    hide_data = st.sidebar.checkbox(label="Afficher les données ")

    if hide_data:
        st.write(df)

    st.sidebar.title("Paramètres")

    feature_selection = st.sidebar.multiselect(label="Choix de la valeur", options=numeric_cols)

    df_features = df[feature_selection]


    plotly_figure = px.line(data_frame=df_features, x=df_features.index, y=feature_selection, title="Chronologie")

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
            tickerDf = tickerData.history(period='id', start=a_date[0].strftime("%Y-%m-%d"), end=a_date[1].strftime("%Y-%m-%d"))
            st.line_chart(tickerDf.Volume)
        else:
            st.write("Chargement...")

###### Calcul de rentabilité journalière
#df.rename(columns = {'Adj Close':'AdjClose'}, inplace = True)

#rents = (df.AdjClose[1:].values - df.AdjClose[:-1].values)/df.AdjClose[1:].values
#rents = pd.Series(rents, index=df.index[1:])

#importation du fichier excel

elif choix=="indicateurs clés":
    st.markdown("<h1 style='text-align: left; color: cadetblue;'>Indicateurs clés</h1>", unsafe_allow_html=True)

    date_cols = data['Date']

    date_selection=st.sidebar.selectbox("Choix date", date_cols)

    #date_selection = st.sidebar.select(label="Choix date", options=date_cols)


    data_renta_mens = data[['Date','rent_month']].dropna()
    data_renta_moy_an = data[['Date','means_rent_year']].dropna()
    Volatilite=data[['Date','volatility']].dropna()
    Dividends=data[['Date', 'Dividends']].dropna()
    
    date_month_cols = data_renta_mens['Date']
    date_year_cols = data_renta_moy_an['Date']


    
    #date_year_selection=st.sidebar.selectbox("Choix date year", date_year_cols)

    value=data[data['Date']==date_selection]
    #rent_year=data_renta_moy_an[data_renta_moy_an['Date']==date_year_selection]
    #vol=Volatilite[Volatilite['Date']==date_selection]

    #print('rent_year', rent_year['means_rent_year'])

    print(value['means_rent_year'].isna())

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

    #st.metric(label="rentabilité mensuelle", value=rent_month['rent_month'], delta="1.2 °F")

    print(date_selection)
    #print(data[data['Date']==date_selection])

   #col1 = st.columns(1)

    #col1.metric("rentabilité mensuelle", data_renta_mens['rent_month'][1], "1.2 °F")
    #col2.metric("rentabilité moyennne annuelle", data_renta_moy_an['means_rent_year'][2], "-8%")
    #col3.metric("Volatilité", Volatilite['volatility'][1], "4%")

elif choix=="Dividende":
    st.markdown("<h1 style='text-align: left; color: cadetblue;'>Dividende</h1>", unsafe_allow_html=True)

    Dividends=data[['Date', 'Dividends']].dropna()
    div = Dividends['Date']
    date_selection=st.sidebar.selectbox("Choix date", div)


    value=Dividends[Dividends['Date']==date_selection]



    st.metric(label=f"Diviende versée à la date du {date_selection}", value=value['Dividends'])





