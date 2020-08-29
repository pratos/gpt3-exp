# flake8: noqa

import re
from pathlib import Path
from time import perf_counter
from typing import Dict

import openai
import streamlit as st
import yaml
from openai.openai_object import OpenAIObject

MODELS = ["davinci", "curie", "babbage", "ada"]
DATASET_PATH = Path(__file__).parents[2] / "gpt3_exp" / "datasets"
GPT3_CONFIG_PATH = Path(__file__).parents[2] / "gpt3_exp" / "gpt3_config.yml"
DATASETS = dict(
    [
        (re.sub(r"_", " ", str(ds).split("/")[-1].split(".yml")[0].title()), ds)
        for ds in list(DATASET_PATH.glob("*.yml"))
    ]
)


def experimentation():
    load_openai_key()
    st.write("(OpenAI key loaded)")

    model = st.sidebar.selectbox("Select OpenAI model:", MODELS)
    st.markdown(f"Model selected: `{model}`")

    max_tokens = st.sidebar.number_input(
        "Max Tokens to generate:", min_value=1, max_value=2048, step=1
    )
    completions = st.sidebar.number_input(
        "Max number of completions:", min_value=1, max_value=2048, step=1
    )
    randomness = st.sidebar.radio("Randomness param:", ["temperature", "top_n"])
    if randomness == "temperature":
        temperature = st.sidebar.number_input("Temperature", min_value=0.0, max_value=1.0)
    elif randomness == "top_n":
        top_n = st.sidebar.number_input("Top N", min_value=0.0, max_value=1.0)

    prime = st.selectbox("Select dataset:", list(DATASETS.keys()))
    st.sidebar.selectbox("Stream output?", [False, True])
    show_input_ds = st.selectbox("Show Input?", [False, True])

    dataset = load_primes(prime=prime)
    prompt = st.text_area("Enter your prompt", value="Enter just the text...")
    submit = st.button("Submit")
    parsed_primes = "".join(list(dataset["dataset"].values()))

    if show_input_ds:
        st.info(f"{parsed_primes}\n\n{dataset['input']}:{prompt}\n{dataset['output']}:")

    if submit:
        with st.spinner("Requesting completion..."):
            ts_start = perf_counter()
            request = openai.Completion.create(
                engine=model,
                max_tokens=max_tokens,
                temperature=temperature,
                best_of=completions,
                stop="\n",
                prompt=f"{parsed_primes}\n\n{dataset['input']}:{prompt}\n{dataset['output']}:",
            )
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
