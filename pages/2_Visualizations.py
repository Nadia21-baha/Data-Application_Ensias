import streamlit as st
import plotly.express as px  # Idéal pour faire des graphiques interactifs pro
import pandas as pd


st.title(" Insights")
st.subheader("Visual Analysis of the App ")
st.divider()
if 'data_concurrents' in st.session_state:
    df_visualisation = st.session_state['data_concurrents']
    mot_cle = st.session_state['search_query']
    st.info(f"--> Showing visualizations for: **'{mot_cle}'**")

    df_visualisation['score'] = pd.to_numeric(df_visualisation['score'], errors='coerce')
    df_visualisation['realInstalls'] = pd.to_numeric(df_visualisation['realInstalls'], errors='coerce')
    df_visualisation['ratings'] = pd.to_numeric(df_visualisation['ratings'], errors='coerce')

    st.markdown("### Market Share: Real Installs per Application")

    fig_bar = px.bar(
        df_visualisation.sort_values(by="realInstalls", ascending=False), 
        x="title", 
        y="realInstalls",
        title="Total Downloads Comparison",
        labels={"realInstalls": "Real Installs", "title": "Application Name"},
        color="realInstalls",
        color_continuous_scale="Purples" # Pour rester dans ton thème violet !
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.divider()

    st.markdown("### User Satisfaction vs. Total Feedback")
    fig_scatter = px.scatter(
        df_visualisation,
        x="ratings",
        y="score",
        size="realInstalls", # Plus l'app a de téléchargements, plus le point est gros !
        hover_name="title",
        title="App Score relative to Number of Ratings",
        labels={"ratings": "Number of Ratings", "score": "Average Score (out of 5)"},
        color="score",
        color_continuous_scale="Plasma"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
else:
    st.warning("⚠️ No data found! Please go to the **1 Results Table** page first to search and load the dataset.")