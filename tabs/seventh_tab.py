import streamlit as st
import pandas as pd
import numpy as np


title = "Conclusion"
sidebar_name = "Conclusion"


def run():

    st.title(title)
    st.markdown("---")
    
    st.subheader("Analyse du trafic")

    st.markdown(
        """
        Nous avons effectué l’analyse des données récoltées par les compteurs vélo afin de visualiser les horaires et les zones d’affluence, comme indiqué dans la fiche projet.
        
        Depuis 2019, nous pouvons constater une très grande hausse du trafic cycliste à Paris, qui peut s’expliquer de plusieurs façons :
        * déploiement de pistes cyclables à Paris
        * conscience écologique et économique de la part des cyclistes
        * l’installation continue de nouvelles bornes Vélib
        * ...
        
        
        Nous avons pu constater que le plus gros du trafic avait lieu :
        
        * en semaine, surtout les mardi et jeudi
        * pendant les heures de pointe, entre 7h et 10h et entre 17h et 20h
        * sur les mois de juin et de septembre
        * sur certains grands axes parisiens : boulevard Sébastopol, bords de Seine, bassin de la Villette
        
        Les jours de vacances n’ont pas une grande influence sur le trafic.
        
        Certains jours fériés voient le trafic diminuer drastiquement (Noël, Jour de l’an) et d’autres ont un comptage proche d’un jour non férié, comme l’Ascension ou le Lundi de Pentecôte.
        
        La température et la pluie n’ont pas un énorme effet sur le trafic cycliste.
        
        Sur les différents modèles de machine learning testés, **le modèle Random Forest Regressor et le modèle Bagging Regressor** sont ceux qui permettent d’obtenir les meilleurs résultats avec des tendances fiables par mois mais moins précises sur un rythme journalier.
        
        Enfin, Prophet permet de visualiser une très légère décroissance du trafic cycliste dans les années à venir. Il s’agira d’un point à vérifier avec le temps.
        
        Suite à notre analyse, nous pouvons donc préconiser à la mairie de Paris :
        * d’installer plus de compteurs, notamment dans certaines zones non prises en compte actuellement (nord-est, ouest, sud, aux abords du périphérique) afin de voir s’il y a beaucoup de trafic entrant et sortant de Paris,
        * de développer de nouvelles pistes cyclables et/ou d’améliorer les pistes actuelles, comme témoigne ce reportage vidéo du Parisien le 16 septembre 2022 :
        """
    )

    
    st.video('https://www.youtube.com/watch?v=r8BJbFiZQEI')

    st.subheader("Challenges du projet")

    st.markdown(
        """
       
        Sur le contenu du jeu de données, basé sur des compteurs installés par la mairie de Paris, nous n’avons qu’une seule variable numérique et des données que sur une période limitée, ce qui ne donne qu’une vision partielle et biaisée de la réalité du trafic cycliste. La durée limitée de treize mois ne permettait pas de réaliser des travaux de machine learning satisfaisants. Environ 30% du fichier initial était inexploitable suite à des valeurs manquantes, nous avons réussi à les compléter en faisant un croisement avec un autre jeu de données de la mairie de Paris. La première phase de preprocessing a donc été assez laborieuse pour avoir un jeu de données complet sans valeur manquante.
        
        Nous avons donc cherché à enrichir le jeu de données avec des sources externes à la recherche de corrélations supplémentaires, sur les jours fériés, les vacances scolaires ou encore la météo. Ces sources externes ont aussi nécessité des travaux de preprocessing. Nous avions également la volonté d’ajouter d’autres jeux de données pour notamment pouvoir comparer le trafic cycliste par rapport au trafic automobile ou en mobilité douce mais nous n’avons pas trouvé de source satisfaisante.
        
        Pour pallier la limite sur la période des données, nous avons intégré des comptages plus récents jusqu’en septembre 2022. Grâce à la mairie de Paris, nous avons également pu intégrer les données des compteurs depuis 2019.
        
        Nous aurions aimé pouvoir répondre aux besoins de la mairie de Paris sur l’existence ou non d’une corrélation entre le trafic cycliste et la fréquentation des transports en commun. A notre grand regret, nous n’avons pas trouvé de données satisfaisantes pour mener cette analyse.

        """
    )

    st.image("https://media.giphy.com/media/3osxYyejfjYLY4PZBK/giphy.gif")
