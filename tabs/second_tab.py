import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image


title = "Jeux de données"
sidebar_name = "Jeux de données"


def run():

    st.title(title)
    st.markdown("---")
    
    
    st.header("Jeu de données principal")
    st.markdown("---")

    st.markdown(
        """
        
        Source : Mairie de Paris en open source sur Paris Data : [Comptage vélo – Données Compteurs](https://opendata.paris.fr/explore/dataset/comptage-velo-donnees-compteurs/information/?disjunctive.id_compteur&disjunctive.nom_compteur&disjunctive.id&disjunctive.name)
        
        Il s’agit d’un jeu de données des **comptages horaires de vélos par compteur et localisation des sites de comptage en J-1 sur 13 mois glissants** mis à la disposition par la mairie de Paris. Le fichier change donc tous les jours, et il fait une taille comprise entre 850 Mo et 1,5 Go.
        
        Nous avons récupéré un premier jeu de données qui s’est étalé sur une période entre le **1er avril 2021 et le 23 mai 2022** et avons effectué la très grande majorité du travail de préprocessing et d’analyse sur cette période. Ce jeu de données initial était composé de 15 colonnes et de 1.103.359 lignes. Nous avons par la suite élargi la période pour augmenter le nombre de données présentes, et donc effectuer de meilleures analyses :
        
        * nous avons réactualisé ces données jusqu’à la date du **9 septembre 2022** pour pouvoir intégrer des données plus récentes ;
        
        * après avoir contacté la mairie de Paris, elle nous a donné accès aux données plus anciennes qui ne sont plus accessibles sur le site Paris Data, ce qui nous a permis de pouvoir récupérer et intégrer les données sur les comptages horaires depuis le **1er janvier 2019**.
        
        Nous arrivons au total à un jeu de données de presque 3 millions de lignes (2.921.383 lignes pour être exact)

        """
    )
    st.header("Jeux de données complémentaires")
    st.markdown("---")
    st.markdown(
        """
        Nous avons ajouté des jeux de données complémentaires pour l'analyse :
        
        * [Comptage vélo - Compteurs](https://parisdata.opendatasoft.com/explore/dataset/comptage-velo-compteurs/information/?disjunctive.id_compteur&disjunctive.nom_compteur&disjunctive.id&disjunctive.name&disjunctive.counter) : il s'agit d'un autre jeu de données de la Mairie de Paris en open data qui nous a été utile pour compléter des informations manquantes dans le jeu de données original ;
        
        * [Le calendrier scolaire](https://www.data.gouv.fr/fr/datasets/le-calendrier-scolaire/) et [Jours fériés en France](https://www.data.gouv.fr/fr/datasets/jours-feries-en-france/) pour voir si les vacances scolaires et les jours fériés avaient un impact sur le trafic des vélos ;
        
        * [Observation météorologique historiques France (SYNOP)](https://public.opendatasoft.com/explore/dataset/donnees-synop-essentielles-omm/information/) qui contient des données météo pour voir l'impact des températures et de la pluie sur le trafic.
        """
    )
    
    
