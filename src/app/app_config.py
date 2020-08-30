# flake8: noqa

import re
from pathlib import Path

import streamlit as st

st.set_option("deprecation.showfileUploaderEncoding", False)

MODELS = ["davinci", "curie", "babbage", "ada"]
DATASET_PATH = Path(__file__).parents[1] / "gpt3_exp" / "datasets"
GPT3_CONFIG_PATH = Path(__file__).parents[1] / "gpt3_exp" / "gpt3_config.yml"
DATASETS = dict(
    [
        (re.sub(r"_", " ", str(ds).split("/")[-1].split(".yml")[0].title()), ds)
        for ds in list(DATASET_PATH.glob("*.yml"))
    ]
)
PARAMS = {}
