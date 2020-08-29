import streamlit as st
from app.pages.experimentation import experimentation
from app.pages.results import results

PAGES = ["Exp Page", "Results dashboard"]
page_select = st.sidebar.radio("Pages", options=PAGES)

if page_select == "Exp Page":
    st.title("GPT3 Experimentation")
    experimentation()
elif page_select == "Results dashboard":
    st.title("Results")
    results()
