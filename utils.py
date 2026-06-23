from google_play_scraper import search, app, reviews, Sort
import pandas as pd 
import time
import streamlit as st
from transformers import pipeline

@st.cache_resource
def charger_modele_sentiment():
    return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")


@st.cache_data
def recuperer_data_apps(query):
    results = search(
        query,
        lang="en",
        country="us",
        n_hits=20
    )
    all_apps = []
    for r in results:
        try:
            app_id = r["appId"]
            
            # Récupération des détails
            details = app(app_id, lang="en", country="us")
            
            # Récupération des reviews
            review_data, continuation_token = reviews(
                app_id, lang="en", country="us", sort=Sort.NEWEST, count=50
            )
            review_list = []
            for rev in review_data:
                review_list.append({
                    "userName": rev.get("userName"),
                    "score": rev.get("score"),
                    "content": rev.get("content"),
                    "at": str(rev.get("at"))
                })
             # On crée la fiche de l'application
            app_data = {
                "appId": details.get("appId"),
                "title": details.get("title"),
                "description": details.get("description"),
                "summary": details.get("summary"),
                "score": details.get("score"),
                "ratings": details.get("ratings"),
                "reviews": details.get("reviews"),
                "installs": details.get("installs"),
                "realInstalls": details.get("realInstalls"),
                "price": details.get("price"),
                "free": details.get("free"),
                "currency": details.get("currency"),
                "developer": details.get("developer"),
                "genre": details.get("genre"),
                "genreId": details.get("genreId"),
                "contentRating": details.get("contentRating"),
                "url": details.get("url"),
                "reviews_data": review_list  # On garde la liste des commentaires dedans
            }
            all_apps.append(app_data)
            time.sleep(1)
        except Exception as e:
            print("Erreur sur l'application :", e)
        df_final = pd.DataFrame(all_apps)
    return df_final


def analyser_sentiments_apps(df_apps):
   # Prend le DataFrame des apps, analyse les commentaires de chaque application,
   # et calcule un score global de sentiment (Pourcentage d'avis positifs).

    if df_apps.empty:
        return df_apps
        
    classifier = charger_modele_sentiment()
    
    list_scores_positifs = []
    
    # On boucle sur chaque application du tableau
    for index, row in df_apps.iterrows():
        reviews = row['reviews_data'] # Liste de dictionnaires [object Object]
        
        # Si l'application n'a aucun commentaire extrait
        if not reviews or len(reviews) == 0:
            list_scores_positifs.append(50.0) # Score neutre par défaut par sécurité
            continue
            
        avis_positifs = 0
        total_avis_analyses = 0
        
        # On extrait le texte de chaque avis pour le donner au modèle ML
        for rev in reviews:
            texte_commentaire = rev.get('content', '')
            
            if texte_commentaire.strip(): # S'il y a du texte
                total_avis_analyses += 1
                try:
                    # Le modèle ML fait sa prédiction ici !
                    prediction = classifier(texte_commentaire[:512])[0] # On limite à 512 caractères max
                    if prediction['label'] == 'POSITIVE':
                        avis_positifs += 1
                except Exception:
                    pass
                    
        # Calcul du taux de satisfaction ML de l'application (en %)
        if total_avis_analyses > 0:
            taux_positif = (avis_positifs / total_avis_analyses) * 100
        else:
            taux_positif = 50.0
            
        list_scores_positifs.append(round(taux_positif, 2))
        
    # On ajoute la nouvelle colonne calculée par le modèle ML dans notre tableau !
    df_apps['sentiment_score'] = list_scores_positifs
    return df_apps


