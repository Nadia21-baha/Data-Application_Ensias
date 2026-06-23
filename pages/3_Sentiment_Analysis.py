import streamlit as st
import plotly.express as px
import pandas as pd
# On importe la fonction ML qu'on a créée dans utils.py
from utils import analyser_sentiments_apps 

st.title("ML-Based Sentiment Analysis")
st.subheader("Hugging Face AI Model Insights on User Reviews")
st.divider()

# 1. On vérifie si on a les données de la recherche dans la session_state
if 'data_concurrents' in st.session_state:
    df_apps = st.session_state['data_concurrents']
    mot_cle = st.session_state['search_query']
    
    st.info(f" Analyzing user sentiment trends for: **'{mot_cle}'**")
    
    # 2. On lance l'analyse de sentiment avec notre modèle ML (Hugging Face)
    with st.spinner("Hugging Face Model processing text reviews... Please wait..."):
        # On exécute la fonction et on récupère le tableau mis à jour avec le sentiment_score
        df_avec_sentiment = analyser_sentiments_apps(df_apps)
    
    st.success("Sentiment analysis completed successfully!")
    

    #  BAR CHART DES SENTIMENTS

    st.markdown("###  App Approval Rate (Positive Sentiment %)")
    st.caption("This chart displays the percentage of positive reviews predicted by the NLP model.")
    
    # On crée un graphique à barres pour comparer les scores de satisfaction de l'IA
    fig_sentiment = px.bar(
        df_avec_sentiment.sort_values(by="sentiment_score", ascending=False),
        x="title",
        y="sentiment_score",
        title="User Satisfaction Score per App (%)",
        labels={"sentiment_score": "Positive Reviews (%)", "title": "Application"},
        color="sentiment_score",
        color_continuous_scale="RdYlGn" # Dégradé Rouge (négatif) -> Jaune -> Vert (positif)
    )
    
    # On fixe l'axe Y entre 0 et 100% pour que ce soit propre
    fig_sentiment.update_yaxes(range=[0, 100])
    st.plotly_chart(fig_sentiment, use_container_width=True)
    
    st.divider()
    

    # OPTIONNEL : TABLEAU DES RÉSULTATS FILTRÉS
   
    st.markdown("### Detailed Sentiment Data")
    # On affiche uniquement les colonnes importantes pour l'analyse
    colonnes_visibles = ['title', 'score', 'sentiment_score', 'realInstalls']
    st.dataframe(df_avec_sentiment[colonnes_visibles])

else:
    # Message de sécurité si l'utilisateur n'a rien cherché en page 1
    st.warning("⚠️ No data found! Please go to the **🔍 1 Results Table** page first to search and load the dataset.")