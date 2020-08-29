import streamlit as st
from app.pages.dashboard import dashboard
from app.pages.experimentation import experimentation
from app.pages.results import results

PAGES = ["Dashboard", "Exp Page", "Results"]
page_select = st.sidebar.radio("Pages", options=PAGES)

if page_select == "Dashboard":
    st.title("Dashboard")
    dashboard()
elif page_select == "Exp Page":
    st.title("GPT3 Experimentation")
    experimentation()
elif page_select == "Results":
    st.title("Results")
    results()
