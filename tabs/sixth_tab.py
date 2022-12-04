import streamlit as st
import pandas as pd
import numpy as np
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly

title = "Prophet"
sidebar_name = "Prophet"
prophet = pd.read_csv('./data/prophet.csv', index_col = 0)   


def run():

    st.title("Prévision du trafic à l'aide de Facebook Prophet")
    st.markdown("---")

    st.markdown(
        """
        Facebook a sorti [Prophet](https://facebook.github.io/prophet/), un outil disponible sur Python et R qui permet de **prédire des données dans le temps** de manière simple, rapide et précise à partir de données existantes. Prophet gère également très bien les **effets saisonniers** et les **valeurs extrêmes**. Il est donc un outil idéal pour notre projet.
        
        Pour utiliser Prophet, nous avons dû isoler **deux colonnes du dataframe** : la date et le comptage quotidien de vélos. Il suffit par la suite de créer une nouvelle **instance Prophet**, de **l’entraîner sur les données existantes** et de **définir une durée de prévision**.
        
        """
    )
    
    st.write(prophet.head(20))
    st.caption('Extrait de notre jeu de données simplifié et optimisé pour Prophet')

    st.markdown(
        """

        À partir de ces données Prophet va générer un nouveau dataframe avec ses prévisions quotidiennes, mais également des estimations hautes et basses qui peuvent être facilement affichés dans un graphique :

        """
    )
    
    m = Prophet()
    m.fit(prophet)
 
    duree = st.slider('Définissez une durée de prédiction (en mois)', 1, 60, 36, help = 'Plus la durée sélectionnée sera grande, moins la fiabilité sera présente')
 
    future = m.make_future_dataframe(periods=30 * duree)
    forecast = m.predict(future)

    fig = plot_plotly(m, forecast)
    fig.update_layout(title_text="Prévisions du trafic par Facebook Prophet")

    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(
        """

        Au vu des données depuis 2019, l'algorithme prévoit un trafic relativement stable dans les prochaines années, avec une légère décroissance. Il arrive néanmoins à bien prédire des baisses de trafic l'été et l'hiver.

        """
    )
    
