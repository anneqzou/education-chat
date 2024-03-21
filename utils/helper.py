
import streamlit as st
import os

llm_models = {
    "OpenAI": ["gpt-3.5-turbo"],
    "AOAI":  ["gpt-35-turbo","gpt-4"],
    "SelfHost": ["THUDM/chatglm3-6b-32k"],
}

def initialize_page_config():
    st.set_page_config(
        page_title="LLMGateway Test Center - powered by Streamlit",
        page_icon=":guardsman:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

def format_output(text: str):
    result_string = text.replace("\\n", "\n")
    return result_string

def initialize_page_session_state():
    if "default_llm_config" not in st.session_state:
        st.session_state["default_llm_config"] = dict()

def initialize_llm_default_parameters_session_state():
    if "temperature" not in st.session_state["default_llm_config"]:
        st.session_state["default_llm_config"].update({"temperature": 0.1})

    if "top_p" not in st.session_state["default_llm_config"]:
        st.session_state["default_llm_config"].update({"top_p": 0.95})

    if "frequency_penalty" not in st.session_state:
        st.session_state["default_llm_config"].update({"frequency_penalty": 0.2})

    if "presence_penalty" not in st.session_state:
        st.session_state["default_llm_config"].update({"presence_penalty": 0.0})

    if "max_tokens" not in st.session_state:
        st.session_state["default_llm_config"].update({"max_tokens": 2000})

def clear_chat_multi_history():

    for llm in llm_models.keys():
        if st.session_state[f"selected_{llm}"]:
            for model in st.session_state[f"selected_{llm}_models"]:
                if model in llm_models[llm]:
                    st.session_state[llm][model]["messages"] = []

def sidebar_for_llm_endpoint(llm):
    
    if llm not in st.session_state:
        st.session_state[llm] = {}

    st.session_state[llm]["base_url"]  = st.text_input(
        "OPENAI BASE URL",
        key=f"{llm}_base_url",
        type="default",
        value=st.session_state[llm].get("base_url", load_config_from_envs(llm, "base_url")),
    )

    st.session_state[llm]["api_key"] = st.text_input(
        "OPENAI API KEY",
        key=f"{llm}_api_key",
        type="password",
        value=st.session_state[llm].get("api_key", load_config_from_envs(llm, "api_key")),
    )

    if llm == "AOAI":
        st.session_state[llm]["api_version"] = st.text_input(
            "OPENAI API VERSION",
            key=f"{llm}_api_version",
            type="default",
            value=st.session_state[llm].get("api_version", load_config_from_envs(llm, "api_version"))
        )

def sidebar_for_llm_parameters(llm, model):

    if model not in st.session_state[llm]:
        st.session_state[llm][model] = {}

    if 'messages' not in st.session_state[llm][model]:
        st.session_state[llm][model]['messages'] = []

    if llm == "AOAI":
        st.session_state[llm][model]["stream_mode"] = st.sidebar.selectbox(
            "stream mode", 
            ["No"], 
            key=f"{llm}_{model}_stream_mode", 
            index=0
        )
    else:
        st.session_state[llm][model]["stream_mode"] = st.sidebar.selectbox(
            "stream mode", 
            ["No", "Yes"], 
            key=f"{llm}_{model}_stream_mode", 
            index=0
        )

    st.session_state[llm][model]["temperature"] = st.sidebar.slider(
        label="temperature",
        key=f"{llm}_{model}_temperature",
        min_value=0.01,
        max_value=5.0,
        value=st.session_state["default_llm_config"]["temperature"],
        step=0.01,
    )

    st.session_state[llm][model]["top_p"] = st.sidebar.slider(
        label="top_p",
        key=f"{llm}_{model}_top_p",
        min_value=0.01,
        max_value=1.0,
        value=st.session_state["default_llm_config"]["top_p"],
        step=0.01,
    )

    st.session_state[llm][model]["frequency_penalty"] = st.sidebar.slider(
        label="frequency_penalty",
        key=f"{llm}_{model}_frequency_penalty",
        min_value=0.0,
        max_value=2.0,
        value=st.session_state["default_llm_config"]["frequency_penalty"],
        step=0.01,
    )

    st.session_state[llm][model]["presence_penalty"] = st.sidebar.slider(
        label="presence_penalty",
        key=f"{llm}_{model}_presence_penalty",
        min_value=0.0,
        max_value=2.0,
        value=st.session_state["default_llm_config"]["presence_penalty"],
        step=0.01,
    )

    st.session_state[llm][model]["max_tokens"] = st.sidebar.slider(
        label="max_tokens",
        key=f"{llm}_{model}_max_tokens",
        min_value=0,
        max_value=16384,
        value=st.session_state["default_llm_config"]["max_tokens"],
        step=8,
    )

    st.divider()

def check_required_parameter(llm):
    if not st.session_state[llm]["base_url"]:
        st.info("Please add your LLM Endpoint to continue.")
        st.stop()

    if not st.session_state[llm]["api_key"]:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    if llm == "AOAI" and not st.session_state[llm]["api_version"]:
        st.info("Please add your Azure API Version to continue.")
        st.stop()

def load_config_from_envs(llm, parameter):
    # override default setting from environment variables
    value = os.environ.get(f"{llm}_{parameter}", "")
    return value
