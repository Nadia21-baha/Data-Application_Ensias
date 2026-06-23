import streamlit as st
from utils import recuperer_data_apps


st.title("Results table:")
st.divider()
query_user=st.text_input("which category you want to analyse ?"
                         ,placeholder=" mental health ai, productivity, fitness...",value=""
                         ,help="Type any keyword to fetch live market data.")
# 3. if the user write smth we search
if query_user:
    st.write(f"Analyzing market trends for: {query_user}...")
    with st.spinner("Connecting API for extracting... this may takes some fex minutes : "):
        df_resultats = recuperer_data_apps(query_user)
    st.success("Données récupérées avec succès !")

    #ze gonna store ower data to share it with the visualization page
    st.session_state['data_concurrents'] = df_resultats
    st.session_state['search_query'] = query_user

    st.markdown(":violet-background[Raw Dataset Overview]")
    df_resultats
else:
    
    st.info("**Please type a keyword in the input box above and press Enter to start analyzing .**")