import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
import branca.colormap as cm
from streamlit_folium import st_folium


title = "Visualisation des données"
sidebar_name = "Visualisation"


def run():

    st.title(title)
    st.markdown("---")
    st.markdown(
        """
        Sur un jeu de données prêt pour exploitation, nous pouvons visualiser différentes graphiques analysant le trafic cycliste listés ci-dessous :
         - Comptage par jour, 
         - Cartographie des compteurs, 
         - Heure, jour, mois, 
         - Vacances, 
         - Jours fériés, 
         - Températures, 
         - Précipitations, 
         - Matrice de corrélation

        """
    )
    st.subheader("Sélectionnez la visualisation souhaitée :")

    option = st.selectbox(
    'Visualisation',
    ('Comptage par jour', 'Cartographie des compteurs', 'Heure, jour, mois', 'Vacances', 'Jours fériés', 'Températures', 'Précipitations', 'Matrice de corrélation'))

    st.subheader(option)
    
    if option == 'Comptage par jour':
        count_per_day = pd.read_csv('./data/count_per_day.csv')
        fig = px.line(count_per_day, x="date_comptage", y="comptage_h")
        moyenne = count_per_day['comptage_h'].mean()
        fig.add_hline(y=moyenne, line_dash = 'dot', annotation_text = 'Moyenne', line_color = 'red')
        fig.update_layout(title = '<b>Courbe du nombre total de vélos par jour', title_x=0.5, xaxis_title = 'Date', yaxis_title = 'Nombre de vélos')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            """
            Nous traçons le nombre de vélos cumulés par jour.
            
            On peut noter une moyenne à 120 000 vélos par jour, et de nombreuses pointes à plus de 250 000 vélos quotidiens.
            
            Hors périodes exceptionnelles (confinement, grèves...), on peut voir des répétitions de motif : il y a moins de vélos pendant le mois d'août et la période de noël et il y a des pics en juin et septembre.
            """
        )
        
        fig = px.box(count_per_day, x="comptage_h")
        fig.update_layout(title='<b>Cumul du comptage horaire par jour', title_x=0.5, yaxis_title='Nombre de vélos')
        st.plotly_chart(fig, use_container_width=True)
        
        
        st.markdown(
            """
            En utilisant un boxplot, nous pouvons voir la réparition des valeurs :
            
            * Le minimum est de 395 vélos comptés sur une journée (le 31 décembre 2019)
            * La médiane est à 120 000 vélos
            * Le maximum est à 285 000 vélos.
            """
        )

    if option == 'Cartographie des compteurs':
        site_map = pd.read_csv('./data/site_map.csv')

        site_map['latitude'] = site_map['latitude'].astype(float)
        site_map['longitude'] = site_map['longitude'].astype(float)

        m3 = folium.Map(location=[48.856613, 2.352222], zoom_start=12, control_scale = True)

        for i in range(len(site_map)):
          lat = site_map['latitude'][i]
          long = site_map['longitude'][i]
          comptage = site_map['comptage_h'][i]
          nom_site = site_map['nom_site'][i]
          if comptage <= 500000:
            couleur='#2aff00'
            taille = 5
          elif(comptage > 500000) & (comptage <= 1500000):
            couleur= '#d2ff00'
            taille = 10
          elif (comptage > 1500000) & (comptage <= 3000000):
            couleur= '#ffb400'
            taille = 20
          else:
            couleur= '#ff0000'
            taille = 30
          #else:
            #couleur= 'purple'
            #taille = 40

          folium.CircleMarker(
              location=[lat, long],
              radius=taille,
              popup=nom_site,
              tooltip = comptage,
              color=couleur,
              fill=True, fill_color=couleur, fill_opacity=0.5).add_to(m3)


        cmp = cm.LinearColormap(['#2aff00', '#ffff00', '#ffb400', '#ff0000'])
        cmp = cmp.to_step(index=[0, 500000, 1500000, 3000000, 5000000])
        cmp.caption = 'Nombre de vélos par site de comptage'
        cmp.add_to(m3)

        st_data = st_folium(m3, width=725)


        st.markdown(
            """
            Nous faisons figurer sur cette carte les différents compteurs installés à Paris. La taille des points et la couleur indiquent leur comptage cumulé depuis 2019.
            
            Nous pouvons voir que les **bords de Seine** et l'**axe Gare du Nord / Châtelet** sont vraiment fréquentés.
            
            Certaines zones sont moins fréquentées : les **abords du périphérique** notamment.
            
            Enfin, il y a des "déserts" sans compteurs : les **16e et  20e arrondissements** par exemple.
            
            Nous pouvons notamment montrer les 5 sites de comptage les plus fréquentés et les moins fréquentés :
            """
        )
        
        fig = px.bar(site_map.sort_values(by = 'comptage_h', ascending=True).tail(5), x='comptage_h', y='nom_site', color = 'comptage_h')
        fig.update_layout(title_text="Les 5 sites de comptage les plus fréquentés")
        st.plotly_chart(fig, use_container_width=True)
        
        fig = px.bar(site_map.sort_values(by = 'comptage_h', ascending=True).head(5), x='comptage_h', y='nom_site', color = 'comptage_h')
        fig.update_layout(title_text="Les 5 sites de comptage les moins fréquentés")
        st.plotly_chart(fig, use_container_width=True)
        

    if option == 'Heure, jour, mois':
        day_count = pd.read_csv('./data/day_count.csv')
        hour_count = pd.read_csv('./data/hour_count.csv')
        datesemaine = pd.read_csv('./data/datesemaine.csv')
        mois_count = pd.read_csv('./data/mois_count.csv')
        
        st.markdown(
            """
            Nous allons maintenant regarder s'il y a des heures de la journée, des jours de la semaine ou des mois plus fréquentés que d'autres.
            """
        )
 
        st.subheader("Par heure :")

 
        fig = px.line(hour_count, x='heure_comptage', y='comptage_h')
        fig.update_layout(title_text="Moyenne du nombre de vélos par compteur et par heure de la journée")
        fig.update_xaxes(dtick="1", title_text = 'Heure')
        fig.update_yaxes(title_text="Nombre de vélos")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            """
            Sans surprise, la fréquentation est plus forte aux **heures de pointe** : entre 8 et 9h le matin et entre 18h et 19h le soir. Il semblerait que le trafic est plus dense en soirée qu'en matinée.
            """
        )

        st.subheader("Par jour de la semaine :")

        
        fig = px.bar(day_count, x='jour_comptage', y='comptage_h', color = 'comptage_h')
        fig.update_layout(title_text="Moyenne du nombre de vélos par compteur et par jour de la semaine")
        fig.update_xaxes(dtick="1", title_text = 'Jour de la semaine')
        fig.update_yaxes(title_text="Nombre de vélos")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            """
            Les vélos sont **plus empruntés les jours de la semaine que le week-end**. On peut combiner heures et jour de la semaine pour voir s'il y a une vraie influence sur les "vélotaffeurs" : circulation accentuée pour aller ou revenir du travail.
            """
        )
        st.subheader("Par heure et par jour de la semaine :")

        fig = px.line(datesemaine, x="heure_comptage", y="comptage_h", color='jour_comptage')
        fig.update_layout(title='Moyenne du nombre de vélos par compteur par heure et par jour',
                           xaxis_title='Heure',
                           yaxis_title='Nombre moyen de vélos')
        fig.update_xaxes(dtick="1")    
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(
            """
            Cette représentation conforte nos idées :
            * en semaine, il y a une plus grande fréquentation aux **heures de pointe**, avec un creux la nuit et en journée. Il semble y avoir plus de trafic cycliste le jeudi.
            * le week-end, il y a moins de vélos, avec un **pic entre 15h et 19h**.
            
            Regardons à présent s'il y a une différence de fréquentation par mois de l'année.
            """
        )
        st.subheader("Par mois :")
        
        fig = px.bar(mois_count, x='mois_comptage', y='comptage_h', color = 'comptage_h')
        fig.update_layout(title_text="Moyenne du nombre de vélos par compteur et par mois")
        fig.update_xaxes(dtick="1", title_text = 'Mois')
        fig.update_yaxes(title_text="Nombre de vélos")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            """
            Le pic de fréquentation a lieu pendant **le mois de septembre puis au mois de juin**.

            A contrario, **le mois d'août et en hiver** (en janvier et février inclus) semblent être les plus calmes.
            """
        )

    if option == 'Vacances':
        conges_count = pd.read_csv('./data/conges_count.csv')


        fig = px.bar(conges_count, x='conges', y='comptage_h', color = 'comptage_h')
        fig.update_layout(title_text="Moyenne du nombre de vélos par compteur les jours de vacances scolaires")
        fig.update_xaxes(dtick="1", title_text = 'Type de jour')
        fig.update_yaxes(title_text="Nombre de vélos")    

        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            """
            Il y a moins de vélos les jours de vacances scolaires.
            """
        )

    if option == 'Jours fériés':
        feries_count = pd.read_csv('./data/feries_count.csv')


        fig = px.bar(feries_count.sort_values(by = 'comptage_h', ascending = True), x='nom_jour_ferie', y='comptage_h', color = 'comptage_h')
        fig.update_layout(title_text="Moyenne du nombre de vélos par compteur les jours fériés")
        fig.update_xaxes(dtick="1", title_text = 'Jour férié')
        fig.update_yaxes(title_text="Nombre de vélos")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            """
            Nous pouvons voir qu’il y a une fréquentation moindre dès qu’un jour est férié : le jour de Noël est le jour de l'année où il y a le moins de vélo avec un peu moins de 15 vélos par heure et par compteur, suivi du 1er janvier (20 vélos) et de la Toussaint (24 vélos). Le lundi de Pentecôte, avec son statut de journée de solidarité, est proche de la normale à 53 vélos par heure et par compteur.
            """
        )


    if option == 'Températures':
        datemeteo = pd.read_csv('./data/datemeteo.csv')
        newferies = pd.read_csv('./data/newferies.csv', index_col = 0)
        newvacs = pd.read_csv('./data/newvacs.csv', index_col = 0)
        newferies['date_comptage'] = pd.to_datetime(newferies['date_comptage'], format = '%Y-%m-%dT%H:%M:%S%z', utc = True).dt.tz_convert('Europe/Paris')

        st.markdown(
            """
            Options d'affichage (peut mettre un peu de temps à charger) :
            """
        )
        
        vacs = st.checkbox('Afficher les vacances')
        feries = st.checkbox('Afficher les jours fériés')

        
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add traces
        fig.add_trace(
            go.Scatter(x=datemeteo['date_heure_comptage'], y=datemeteo['comptage_h'], name="Nombre de vélos"),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(x=datemeteo['date_heure_comptage'], y=datemeteo['temp'], name="Température", opacity=.7),
            secondary_y=True,
        )

        # Add figure title
        fig.update_layout(
            title_text="Nombre de vélos et température moyenne par jour depuis janvier 2019",
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            height = 800
        )

        # Set x-axis title
        fig.update_xaxes(title_text="Date")

        # Set y-axes titles
        fig.update_yaxes(title_text="Nombre de vélos", secondary_y=False)
        fig.update_yaxes(title_text="Température", secondary_y=True)

        fig.update_xaxes(rangeslider_visible=True)
        
        if vacs:

            for i in range(len(newvacs)):
              fig.add_vrect(x0=newvacs['start_date'][i], x1 = newvacs['end_date'][i],
                          annotation_text=newvacs['description'][i], annotation_position="top left",
                          annotation_font_size=10,
                          fillcolor="green", opacity=0.25, line_width=0.1)
        
        if feries:

            for j in range(len(newferies)):
              fig.add_vline(x=newferies['date_comptage'][j].timestamp() * 1000, line_color="black", line_width=1.5, line_dash = 'dot',
                            annotation_text=newferies['nom_jour_ferie'][j], annotation_position = "bottom right", annotation_font_size = 10)
                        
                        
                        
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            """
            Nous pouvons facilement identifier les périodes estivales et hivernales sur ce graphique en voyant les hausses et baisses de température. A partir de mi-2020, il semble y avoir un semblant de corrélation sur les températures et le trafic : quand la température remonte, le trafic semble augmenter ; quand la température diminue, le trafic semble diminuer.
            """
        )

 
    if option == 'Précipitations':
        datemeteo = pd.read_csv('./data/datemeteo.csv')
        newferies = pd.read_csv('./data/newferies.csv', index_col = 0)
        newvacs = pd.read_csv('./data/newvacs.csv', index_col = 0)
        newferies['date_comptage'] = pd.to_datetime(newferies['date_comptage'], format = '%Y-%m-%dT%H:%M:%S%z', utc = True).dt.tz_convert('Europe/Paris')
        st.markdown(
            """
            Options d'affichage (peut mettre un peu de temps à charger) :
            """
        )

        vacs = st.checkbox('Afficher les vacances')
        feries = st.checkbox('Afficher les jours fériés')


        
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add traces
        fig.add_trace(
            go.Scatter(x=datemeteo['date_heure_comptage'], y=datemeteo['comptage_h'], name="Nombre de vélos"),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(x=datemeteo['date_heure_comptage'], y=datemeteo['pluie'], name="Précipitations", opacity=.7, line_color = 'orange'),
            secondary_y=True,
        )

        # Add figure title
        fig.update_layout(
            title_text="Nombre de vélos et précipitations par jour depuis janvier 2019",
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            height = 800
        )

        # Set x-axis title
        fig.update_xaxes(title_text="Date")

        # Set y-axes titles
        fig.update_yaxes(title_text="Nombre de vélos", secondary_y=False)
        fig.update_yaxes(title_text="Précipitations", secondary_y=True)

        fig.update_xaxes(rangeslider_visible=True)
        
        if vacs:

            for i in range(len(newvacs)):
              fig.add_vrect(x0=newvacs['start_date'][i], x1 = newvacs['end_date'][i],
                          annotation_text=newvacs['description'][i], annotation_position="top left",
                          annotation_font_size=10,
                          fillcolor="green", opacity=0.25, line_width=0.1)
         
        if feries:

            for j in range(len(newferies)):
              fig.add_vline(x=newferies['date_comptage'][j].timestamp() * 1000, line_color="black", line_width=1.5, line_dash = 'dot',
                            annotation_text=newferies['nom_jour_ferie'][j], annotation_position = "bottom right", annotation_font_size = 10)
                        
                        
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            """
            En revanche, la pluie semble avoir un impact plus important sur la fréquentation. La matinée du 4 juin 2021 a été très pluvieuse et a clairement fait baisser le trafic des vélos. Pareil pour le 8 avril 2022 où il a plu une grande partie de la journée et où la fréquentation a été basse.
            """
        )

    if option == 'Matrice de corrélation':
 

        st.image(Image.open("assets/matrice-correlation.png"))
        st.caption('Matrice de corrélation des différentes variables')



        st.markdown(
            """
            La matrice de corrélation ne nous montre pas une forte corrélation entre les variables. Il ne nous semble pas utile de poursuivre plus loin notre analyse de données.
            """
        )
