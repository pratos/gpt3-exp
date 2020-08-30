# flake8: noqa

import re
from pathlib import Path
from time import perf_counter
from typing import Dict

import openai
import streamlit as st
import yaml
from openai.openai_object import OpenAIObject

st.set_option("deprecation.showfileUploaderEncoding", False)

MODELS = ["davinci", "curie", "babbage", "ada"]
DATASET_PATH = Path(__file__).parents[2] / "gpt3_exp" / "datasets"
GPT3_CONFIG_PATH = Path(__file__).parents[2] / "gpt3_exp" / "gpt3_config.yml"
DATASETS = dict(
    [
        (re.sub(r"_", " ", str(ds).split("/")[-1].split(".yml")[0].title()), ds)
        for ds in list(DATASET_PATH.glob("*.yml"))
    ]
)
PARAMS = {}


def experimentation():
    select_option = st.sidebar.radio("Load key:", ["Add your own", "Load local config"])
    if select_option == "Add your own":
        key_added = st.sidebar.text_area("Add OpenAI key:")
        key_submit = st.sidebar.button("Submit key")
        if key_submit:
            openai.api_key = key_added
            st.write("(OpenAI key loaded)")
    elif select_option == "Load local config":
        load_local = st.sidebar.button("Load local config")
        if load_local:
            load_openai_key()
            st.write("(OpenAI key loaded)")

    PARAMS["engine"] = st.sidebar.selectbox("Select OpenAI model(`engine`):", MODELS)
    st.markdown(f"Model selected: `{PARAMS['engine']}`")

    PARAMS["max_tokens"] = st.sidebar.number_input(
        "Max Tokens to generate(`max_tokens`):", min_value=1, max_value=2048, step=1
    )
    PARAMS["best_of"] = st.sidebar.number_input(
        "Max number of completions(`best_of`):", min_value=1, max_value=2048, step=1
    )
    randomness = st.sidebar.radio("Randomness param:", ["temperature", "top_n"])
    if randomness == "temperature":
        PARAMS["temperature"] = st.sidebar.number_input(
            "Temperature", min_value=0.0, max_value=1.0
        )
    elif randomness == "top_n":
        PARAMS["top_p"] = st.sidebar.number_input(
            "Top P (Alternative sampling to `temperature`)", min_value=0.0, max_value=1.0
        )

    PARAMS["stream"] = st.sidebar.selectbox("Stream output?(`stream`)", [False, True])
    show_input_ds = st.selectbox("Show Input?", [False, True])
    PARAMS["stop"] = st.sidebar.text_input("Stop sequence value(`stop`)")
    PARAMS["presence_penalty"] = st.sidebar.number_input(
        "Presence penalty(`presence_penalty`)", min_value=0.0, max_value=1.0
    )
    PARAMS["frequency_penalty"] = st.sidebar.number_input(
        "Frequency penalty(`frequence_penalty`)", min_value=0.0, max_value=1.0
    )
    PARAMS["logprobs"] = st.sidebar.number_input(
        "Log probability(`logprobs`)", min_value=0.0, max_value=1.0
    )

    dataset = []
    prime_type = st.radio("Select dataset", ["Examples", "Upload own"])
    if prime_type == "Examples":
        prime = st.selectbox("Select dataset:", list(DATASETS.keys()))
        dataset = load_primes(prime=prime)
    elif prime_type == "Upload own":
        try:
            file_string = st.file_uploader("Upload dataset", type=["yaml", "yml"])
            dataset = yaml.safe_load(file_string)
            st.success("Uploaded successfully")
        except Exception:
            st.error(f"[ERROR]:: {e}")

    prompt = st.text_area("Enter your prompt(`prompt`)", value="Enter just the text...")
    submit = st.button("Submit")
    parsed_primes = "".join(list(dataset["dataset"].values()))

    if show_input_ds:
        st.info(f"{parsed_primes}\n\n{dataset['input']}:{prompt}\n{dataset['output']}:")

    PARAMS[
        "prompt"
    ] = f"{parsed_primes}\n\n{dataset['input']}:{prompt}\n{dataset['output']}:"
    if submit:
        with st.spinner("Requesting completion..."):
            ts_start = perf_counter()
            request = openai.Completion.create(**PARAMS)
            ts_end = perf_counter()
        st.write(request)
        st.error(f"Took {round(ts_end - ts_start, 3)} secs to get completion/s")
        save_results(
            result=request, time_in_secs=round(ts_end - ts_start, 3), og_dataset=dataset
        )


def load_primes(prime: str) -> Dict:
    with open(DATASETS[prime], "r") as file_handle:
        dataset = yaml.safe_load(file_handle)

    return dataset


def load_openai_key():
    with open(GPT3_CONFIG_PATH, "r") as file_handle:
        openai.api_key = yaml.safe_load(file_handle)["GPT3_API"]


def save_results(result: OpenAIObject, time_in_secs: float, og_dataset: Dict):
    st.write("Saved successfully to DB")
