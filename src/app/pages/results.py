from pathlib import Path

import streamlit as st

IMAGE_PATH = Path(__file__).parents[2] / "assets"


def results():
    st.image(f"{IMAGE_PATH}")
