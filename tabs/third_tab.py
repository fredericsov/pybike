import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

title = "Analyse exploratoire"
sidebar_name = "Analyse exploratoire"
df_extract = pd.read_csv('./data/df_extract.csv', index_col = 0)   
df_full_extract = pd.read_csv('./data/df_full_extract.csv', index_col = 0)


def run():

    st.title(title)
    st.markdown("---")
    
    st.header("Exploration du jeu de données principal")
    st.markdown("---")

    st.markdown(
        """
        Voici un extrait du jeu de données principal de la mairie de Paris.
        """
    )

    st.write(df_extract)
    st.caption('Extrait du jeu de données principal')

    st.markdown(
    """
    Le jeu de données est composé d'une quinzaine de colonnes avec des informations plus ou moins pertinentes.
    
    Nous ne gardons que certaines colonnes, notamment pour alléger au maximum le jeu de données :
    
    * Identifiant du compteur
    * Nom du compteur
    * Identifiant du site de comptage
    * Nom du site de comptage
    * ***Comptage horaire***, qui est la variable cible
    * Date et heure de comptage
    * Date d'installation du site de comptage
    * Coordonnées géographiques
    """)
    st.header("Valeurs manquantes")
    st.markdown("---")
    
    st.markdown(
    """
    Après avoir ajouté au dataset les valeurs depuis 2019 et effectué une réactualisation à septembre 2022, nous avons tracé une heatmap pour visualiser les valeurs manquantes :
    """)
    
    st.image(Image.open("assets/heatmap-missing-values.png"))
    st.caption('Heatmap des valeurs manquantes')

    st.markdown(
    """
    Nous constatons que **trois colonnes sont toujours complétées** :
    
    * Nom du compteur
    * Comptage horaire
    * Date et heure de comptage
    
    Quand une valeur est manquante dans une des autres colonnes, elle l'est également sur toutes les autres colonnes.
    
    Nous pouvons également voir des valeurs manquantes supplémentaires sur la colonne "Date d'installation du site de comptage".
    
    Pour compléter ces valeurs manquantes, nous nous sommes servis d'un autre jeu de données distribué par la mairie de Paris ([Comptage vélo - Compteurs](https://parisdata.opendatasoft.com/explore/dataset/comptage-velo-compteurs/information/?disjunctive.id_compteur&disjunctive.nom_compteur&disjunctive.id&disjunctive.name&disjunctive.counter)) qui contient les informations référentielles pour combler les valeurs manquantes. En fusionnant les données de ces deux fichiers en utilisant comme clé de jointure la colonne **Nom du compteur** et en corrigeant les adresses mal renseignées dans cette colonne, nous parvenons à n'avoir **plus aucune valeur manquante dans le jeu de données**.
    """)
    
    st.header('Etude statistique de la variable "Comptage horaire"')
    st.markdown("---")
   
    st.markdown(
    """

    
    Nous avons tracé un premier boxplot pour analyser les valeurs que peut prendre la colonne “**Comptage horaire**” et vérifier s’il y a des valeurs aberrantes.
    """)
    
    st.image(Image.open("assets/comptage-horaire.png"))
    st.caption('Représentation du comptage horaire sous forme de boxplot')

    st.markdown(
    """
    **La très grande majorité des valeurs est inférieure à 1500**, mais il y a 4 valeurs qui sont supérieures à 2000 et que nous allons vérifier plus spécifiquement :
    
    * 27 boulevard Diderot le **14 Mars 2021 à 3h** avec un comptage à **2088 vélos/h**, soit **34 vélos par minute**
    
    * 39 Quai François Mauriac le **8 Août 2022 à 1h, puis à 11h et 12h**, avec une pointe à **7781 vélos/h**, soit **130 vélos par minute**
    
    Ces valeurs nous semblent invraisemblables et nous allons donc supprimer ces 4 lignes contenant des outliers. En effet le lieu, les horaires et la période de l'année nous laissent penser que cela relève d'erreur du site de comptage.
    
    Autrement, un minimum de 0 vélo/heure/site et un maximum de 1 302 (soit 21 vélos/minute/site) ne sont pas aberrants. Donc nous gardons toutes les valeurs inférieures ou égales à ce comptage.
    
    """)
    
    
    st.header('Ajout de variables')
    st.markdown("---")
   
    st.markdown(
    """

    Pour nous aider dans l'analyse, nous ajoutons plusieurs variables :
    
    * date
    * heure
    * jour
    * semaine
    * mois
    * année
    * latitude
    * longitude
    
    Nous ajoutons également des variables externes grâce à des jeux de données importés :
    
    * vacances scolaires
    * jours fériés
    * température
    * précipitations
    """)
    
    st.markdown(
        """
        Voici un extrait du jeu de données final :
        """
    )

    st.write(df_full_extract)
    st.caption('Extrait du jeu de données final')

