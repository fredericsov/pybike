import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

title = "Projet VELIB “PyBike”"
sidebar_name = "Introduction"

traffic_reel = pd.read_csv('./data/dataviz_traffic_reel.csv')
traffic_best_predit = pd.read_csv('./data/dataviz_traffic_RandomForestRegressor.csv')

def run():

    # TODO: choose between one of these GIFs
    # st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/1.gif")
    # st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/2.gif")
    st.image("https://media.giphy.com/media/fUAl37gtrfIWgVTiri/giphy.gif")
    # st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/3.gif")

    st.title(title)

    st.markdown("---")

    st.markdown(
        """
        D’après un article du journal « Le Monde » publié le 21 Septembre 2021 "*[A Paris, aux heures de pointe, les vélos sont plus nombreux que les voitures sur certains axes](https://www.lemonde.fr/les-decodeurs/article/2021/09/19/a-paris-aux-heures-de-pointe-les-velos-sont-plus-nombreux-que-les-voitures-sur-certains-axes_6095203_4355770.html)*". Autant dire que ce sujet est important pour la capitale. La Ville de Paris déploie depuis plusieurs années des compteurs à vélo permanents pour évaluer le développement de la pratique cycliste.

Ce projet a pour objectif d’effectuer une étude des données récoltées par ces compteurs vélo à partir du jeu de données des comptages horaires de vélos par compteur et localisation des sites de comptage en J-1 sur 13 mois glissants, mis à disposition en open source par la Ville de Paris.

Ces données vont nous permettre de réaliser des analyses sur le nombre de vélos par site de comptage, par date et heure ainsi que par date d’installation des sites de comptage.

Nous pouvons ainsi réaliser des outils d’interprétation : Cartographie, Disparités entre zones géographiques, Fréquentation, Disponibilité… qui permettront à la mairie de Paris d’envisager les améliorations à apporter sur les différents endroits cyclables de la Métropole.
        """
    )


    st.markdown("---")

    st.header("Données")

    st.markdown(
        """
        **Fichier principal :**
        
Source : Mairie de Paris en open source sur Paris Data
Comptages horaires de vélos par compteur et localisation des sites de comptage en 
J-1 sur 13 mois glissants (entre le 1er avril 2021 et le 23 mai 2022)
- → Fichier original de 900 Mo
- → 15 colonnes et 1.103.359 lignes



**Ajout de données depuis 2019 et Mise à jour :**

- Intégration des données sur les comptages horaires depuis le 1er janvier 2019
- Actualisation des données jusqu’à la date du 9 septembre 2022 
- → Jeu de données final de presque 3 millions de lignes, soit environ 2 million de données ajoutées en plus 

**Ajout de variables externes :**
- Vacances Scolaires
- Jours fériés
- Météo

        """
    )

  


    st.markdown("---")

    st.header("Algorithmes de machine learning")

    st.subheader("Démarche")

    st.markdown(
        """

        - **Objectif :** de prédire le nombre de vélos moyen par jour, nous allons donc utiliser des modèles de régression.

        - **Contrainte :** Aucune des 20 variables du dataset n'est numérique

        - **Méthode :** créer 29 variables explicatives numériques, dérivées de jour et mois de comptage ( *une variable/jour de la semaine & une variable/mois de l'année* ).

        """
    )

    st.subheader("Modèles et Prédictions")

    st.markdown(
        """

        - **Modèle choisi : RandomForestRegressor**, le plus robuste parmi les 8 modèles de régression testés.

        - **Résultats :** R² test/train : 0.80 / 0.98 - RMSE test/train : 11.49 / 3.86

        - **Représentation graphique :** 

        """
    )

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scattergl(x=traffic_reel['date_comptage'], y=traffic_reel['comptage_h'], name="Nombre de vélos réel"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scattergl(x=traffic_best_predit['date_comptage'], y=traffic_best_predit['comptage_predit'], name="Nombre de vélos predit RFG", opacity=.7, line_color="#c239c4"),
        secondary_y=True,
    )

    
    # Add figure title
    fig.update_layout(
        title_text="<b>Nombre de vélos par jour</b>", title_x=0.5
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Date")

    # Set y-axes titles
    fig.update_yaxes(title_text="Nombre de vélos réel/prédit", secondary_y=False)
    fig.update_yaxes(title_text="Date", secondary_y=True)

    fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
    ))

    fig.update_xaxes(rangeslider_visible=True)

    st.plotly_chart(fig, use_container_width=True) 
    st.subheader("Conclusion")

    st.markdown(
        """

        - Les prédictions du modèle Random Forest Regressor semblent fiables sur la tendance par mois.

        - Elles sont moins précises sur un rythme journalier

        - **Il semble difficile de prédire précisément le nombre de vélos par jour avec les données analysées**

        """
    )