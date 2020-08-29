from pathlib import Path

import streamlit as st

IMAGE_PATH = Path(__file__).parents[3] / "assets"


def results():
    st.subheader("Waiting to be implemented...")
    st.image(f"{IMAGE_PATH / 'waiting.gif'}")
