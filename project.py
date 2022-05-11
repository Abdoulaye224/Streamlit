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


st.title("Tableau de bord de suivi d'actif ")
st.markdown('Pour la période de **mai 2017** à **mai 2022**.')

pages=["Accueil", "Cours boursiers", "indicateurs clés", "Dividende"]
choix=st.sidebar.selectbox("Menu", pages)

image = Image.open('home.PNG')

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
    st.markdown("<h1 style='text-align: left; color: cadetblue;'>ACCUEIL</h1>", unsafe_allow_html=True)
    st.image(image)

elif choix=="Cours boursiers":

    hide_data = st.sidebar.checkbox(label="Afficher les données ")

    if hide_data:
        st.write(df)

    st.sidebar.title("Paramètres")

    feature_selection = st.sidebar.multiselect(label="Choix", options=numeric_cols)

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
    df.rename(columns = {'Adj Close':'AdjClose'}, inplace = True)

    rents = (df.AdjClose[1:].values - df.AdjClose[:-1].values)/df.AdjClose[1:].values
    rents = pd.Series(rents, index=df.index[1:])

    st.write(rents)



