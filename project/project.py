from cProfile import label
from cgitb import text
from contextlib import nullcontext
from optparse import Option
from turtle import title
from unicodedata import numeric
import pandas as pd
import streamlit as st
import plotly.express as px
#import numpy as np

#La fonction pour charger les données
def load_data():
    df = pd.read_csv("ENGIY.csv", index_col='Date')

    numeric_df = df.select_dtypes(['float', 'int'])
    numeric_cols = numeric_df.columns

    text_df = df.select_dtypes(['object'])
    text_cols = text_df.columns


    return df, numeric_cols, text_cols


df, numeric_cols, text_cols = load_data()


st.title("Tableau de bord de suivi d'actif ")
st.markdown('Réaliser par **Ahmed** and **Abdou**.')

#L'affichage du tableau des valeurs

hide_data = st.sidebar.checkbox(label="Afficher les données ")

if hide_data:
    st.write(df)

#titre 
st.sidebar.title("Paramètres")

feature_selection = st.sidebar.multiselect(label="Features to plot", options=numeric_cols)

print(feature_selection)

df_features = df[feature_selection]

plotly_figure = px.line(data_frame=df_features, x=df_features.index, y=feature_selection, title="test")
#stock_dropdown = st.sidebar.selectbox(label="Stock Ticker")

st.plotly_chart(plotly_figure)

