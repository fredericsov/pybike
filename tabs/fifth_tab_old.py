from random import shuffle
import streamlit as st
import pandas as pd
import numpy as np
#on prépare la data et le target
from sklearn.model_selection import train_test_split

from sklearn.preprocessing import StandardScaler

# pour le calcul de MSE, MAE
from sklearn.metrics import mean_squared_error, mean_absolute_error

# LinearRegression, Lasso, Ridge, ElasticNetCV
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNetCV
 
#DecisionTreeRegressor
from sklearn.tree import DecisionTreeRegressor

#AdaBoostRegressor, BaggingRegressor, RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor, BaggingRegressor, RandomForestRegressor

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


title = "Modélisation & Prédictions"
sidebar_name = "Modélisation & Prédictions"
ml = pd.read_csv('./data/ml_dataset.csv') 

def run():

    st.title(title)
    st.markdown("---")

    
    tab1, tab2, tab3 = st.tabs(["Préparation des données", "Récap des modèles créés", "Analyse du meilleur modèle"])

    with tab1:
        st.header("Préparation des données")

        X = ml.drop('comptage', axis=1)
        Y = ml['comptage']

        st.markdown(f'<h1 style="color:#661d6d;font-size:24px;">{"Choississez les variables"}</h1>', unsafe_allow_html=True)
        Xlistcol = st.multiselect(
        '',
        X.columns.values,
        X.columns.values)
        
        X = X[Xlistcol]
        st.write(X.head(10))

        st.markdown(f'<h1 style="color:#661d6d;font-size:24px;">{"Choississez le pourcentage à alouer pour le test dataset"}</h1>', unsafe_allow_html=True)

        
        value = st.slider("", 10, 40, 20)
        st.write('% Train :', 100-value, ',  % Test :', value)

        

        st.markdown(f'<h1 style="color:#661d6d;font-size:24px;">{"Choix du paramètre shuffle"}</h1>', unsafe_allow_html=True)
        shuffle_value = st.radio(
                            "",
                            ('False', 'True'))
        if shuffle_value == 'False':
            st.write('Vous avez choisi shuffle=False')
        else:
            st.write("Vous avez choisi shuffle=True")

        # on split les données pour le train et le test 
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=(value/100), shuffle=shuffle_value)

        st.markdown(f'<h1 style="color:#661d6d;font-size:24px;">{"Choix de la normalisation des données"}</h1>', unsafe_allow_html=True)
        sc_value = st.radio(
                            "",
                            ('True', 'False'))
        if sc_value == 'True':
            st.write('Vous avez choisi de normaliser les données')
            
            # on normalise les différents sets de data
            cols = X.columns
            sc = StandardScaler()
            X_scaled = sc.fit_transform(X[cols])
            X_train[cols] = sc.fit_transform(X_train[cols])
            X_test[cols] = sc.transform(X_test[cols])
        else:
            st.write("Vous avez choisi de ne pas normaliser les données.")
            X_scaled = X
        
        

        # on vérifie la répartition
        st.markdown(f'<h1 style="color:#661d6d;font-size:24px;">{"Répartition des données du train et test dataset:"}</h1>', unsafe_allow_html=True)
        
        st.write('X_train:',X_train.shape,', X_test:', X_test.shape)
        st.write('Y_train:',Y_train.shape,', Y_test:',Y_test.shape)

        

    with tab2:
        st.header("Récap des modèles créés")
        MLModels = [
                    ["LinearRegression",LinearRegression],
                    ["Lasso",Lasso],
                    ["Ridge",Ridge],
                    ["ElasticNetCV",ElasticNetCV],
                    ["AdaBoostRegressor",AdaBoostRegressor],
                    ["BaggingRegressor",BaggingRegressor],
                    ["DecisionTreeRegressor",DecisionTreeRegressor],
                    ["RandomForestRegressor",RandomForestRegressor]
                    ]
        
        cols = ['Model','R2_test','R2_train','RMSE_test','RMSE_train','MSE_test','MSE_train','MAE_test','MAE_train']
        lst_result = []
        
        
        for modelname, model in MLModels:
            #ModelName = y.split("(",1)[0]    
            if modelname == "ElasticNetCV":
                MLModel = model(cv=8, l1_ratio=(0.1, 0.25, 0.5, 0.7, 0.75, 0.8, 0.85, 0.9, 0.99), alphas=(0.001, 0.01, 0.02, 0.025, 0.05, 0.1, 0.25, 0.5, 0.8, 1.0))
                
            if  modelname == "AdaBoostRegressor" or modelname == "BaggingRegressor" :
                MLModel = model(n_estimators=500)
                
            else:
                MLModel = model()
    
            MLModel.fit(X_train, Y_train)
            y_pred = MLModel.predict(X_test)
            y_train_pred = MLModel.predict(X_train)

            lst_result.append([modelname, round(MLModel.score(X_test, Y_test),3), round(MLModel.score(X_train, Y_train),3), 
                            round(np.sqrt(mean_squared_error(Y_test, y_pred)),2), round(np.sqrt(mean_squared_error(Y_train, y_train_pred)),2),
                            round(mean_squared_error(Y_test, y_pred),2), round(mean_squared_error(Y_train, y_train_pred),2),
                            round(mean_absolute_error(Y_test, y_pred),2), round(mean_absolute_error(Y_train, y_train_pred),2) ])

        y_all = MLModel.predict(X_scaled)

        df_result = pd.DataFrame(lst_result, columns=cols)
        df_result = df_result.sort_values(by=['R2_test','RMSE_test'], ascending=[False, False])
        style = df_result.style.hide_index()
        st.write(style.to_html(), unsafe_allow_html=True)
        bestmodel = 'Le meilleur modèle est ' + df_result.iloc[0]['Model']
        #st.write(bestmodel)

        st.markdown(f'<h1 style="color:#661d6d;font-size:24px;">{bestmodel}</h1>', unsafe_allow_html=True)
    

    with tab3:
        st.header("Analyse du meilleur modèle")

        datavizmodel = 'Représentation graphique avec le meilleur modèle ' + df_result.iloc[0]['Model']
        st.markdown(f'<h1 style="color:#661d6d;font-size:24px;">{datavizmodel}</h1>', unsafe_allow_html=True)

        traffic_reel = pd.read_csv('./data/count_per_day.csv')
        traffic_predit = pd.DataFrame(columns = ['date_comptage', 'comptage_predit'])

        for modelname, model in MLModels:
            if modelname == df_result.iloc[0]['Model']:
                
                if modelname == "ElasticNetCV":
                    MLModel = model(cv=8, l1_ratio=(0.1, 0.25, 0.5, 0.7, 0.75, 0.8, 0.85, 0.9, 0.99), alphas=(0.001, 0.01, 0.02, 0.025, 0.05, 0.1, 0.25, 0.5, 0.8, 1.0))
                
                if  modelname == "AdaBoostRegressor" or modelname == "BaggingRegressor" :
                    MLModel = model(n_estimators=500)

                else:
                    MLModel = model()

            MLModel.fit(X_train, Y_train)
            y_all = MLModel.predict(X_scaled)
            traffic_predit['date_comptage'] = traffic_reel['date_comptage']
            traffic_predit['comptage_predit'] = pd.Series(y_all)
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add traces
        fig.add_trace(
            go.Scattergl(x=traffic_reel['date_comptage'], y=traffic_reel['comptage_h'], name="Nombre de vélos réel"),
            secondary_y=False,
        )

        #fig.add_trace(
        #    go.Scattergl(x=traffic_best_predit['date_comptage'], y=traffic_best_predit['comptage_predit'], name="Nombre de vélos predit RFG", opacity=.7, line_color="#c239c4"),
        #    secondary_y=True,
        #)

        fig.add_trace(
            go.Scattergl(x=traffic_predit['date_comptage'], y=traffic_predit['comptage_predit'], name="Nombre de vélos predit", opacity=.7, line_color="#eda70e"),
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
        ), height = 600)

        fig.update_xaxes(rangeslider_visible=True)

        st.plotly_chart(fig, use_container_width=True)  