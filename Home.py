import streamlit as st

st.set_page_config(
    page_title="Competitor & Sentiment Analysis App",
    page_icon=":=)",
    layout="wide"
)



st.title("Data-Application_Ensias")
st.write("Made by :    Nadia Baha ")
st.markdown("### *Welcome to your Business Intelligence & Analytics Dashboard*")

st.divider()
col1, col2 = st.columns(2)
with col1:
    st.write(" ")
    st.header("Key Features")
    st.markdown("""
    - **Search for Apps**: Permet de rechercher des applications...
    - **Data Visualizations**: Permet de voir des graphiques ...
    - **Sentiment Analysis**: Faire une analyse ...
     """)
with col2:
   
    st.header("How to use the app ?")
    st.markdown(":red-background[Use the sidebar to naviguate]")
    st.write("1. Go to **Results_Table**.")
    st.write("2.write what you want to research (like: mental health ai ...) and validate.")
    st.write("3.view the table and go to **Visualizations** et **Sentiment Analysis** to visualize the results !")

