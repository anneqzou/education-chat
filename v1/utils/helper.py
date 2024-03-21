import streamlit as st

def format_output(text: str):
    result_string = text.replace("\\n", "\n")
    return result_string

def clear_chat_history(pagename):
    if pagename in st.session_state:
        st.session_state[pagename]["messages"] = [
            {"role": "assistant", "content": "How can I help you?"}
        ]

def clear_chat_multi_history(pagename):
    if pagename in st.session_state:
        st.session_state[pagename]["messages"] = [
        ]

def initialize_page_session_state(pagename, default_values):
    if pagename not in st.session_state:
        st.session_state[pagename] = default_values


def initialize_llm_parameters_session_state(pagename: str):
    if "temperature" not in st.session_state[pagename]:
        st.session_state[pagename].update({"temperature": 0.1})

    if "top_p" not in st.session_state[pagename]:
        st.session_state[pagename].update({"top_p": 0.95})

    if "frequency_penalty" not in st.session_state:
        st.session_state[pagename].update({"frequency_penalty": 0.2})

    if "presence_penalty" not in st.session_state:
        st.session_state[pagename].update({"presence_penalty": 0.0})

    if "max_tokens" not in st.session_state:
        st.session_state[pagename].update({"max_tokens": 4096})


def sidebar_for_llm_parameters(pagename: str):
    st.session_state[pagename]["stream_mode"] = st.sidebar.selectbox(
        "Stream Mode", ["No", "Yes"], key="stream_mode", index=0
    )

    st.session_state[pagename]["temperature"] = st.sidebar.slider(
        "temperature",
        min_value=0.01,
        max_value=5.0,
        value=st.session_state[pagename]["temperature"],
        step=0.01,
    )

    st.session_state[pagename]["top_p"] = st.sidebar.slider(
        "top_p",
        min_value=0.01,
        max_value=1.0,
        value=st.session_state[pagename]["top_p"],
        step=0.01,
    )

    st.session_state[pagename]["frequency_penalty"] = st.sidebar.slider(
        "frequency_penalty",
        min_value=0.0,
        max_value=2.0,
        value=st.session_state[pagename]["frequency_penalty"],
        step=0.01,
    )

    st.session_state[pagename]["presence_penalty"] = st.sidebar.slider(
        "presence_penalty",
        min_value=0.0,
        max_value=2.0,
        value=st.session_state[pagename]["presence_penalty"],
        step=0.01,
    )

    st.session_state[pagename]["max_tokens"] = st.sidebar.slider(
        "max_tokens",
        min_value=0,
        max_value=16384,
        value=st.session_state[pagename]["max_tokens"],
        step=8,
    )


def sidebar_for_openai_endpoint(pagename: str):
    
    st.session_state[pagename]["openai_model"] = st.sidebar.selectbox(
        "Choose the model", ["gpt-3.5-turbo"], key="openai_model", index=0
    )

    st.session_state[pagename]["openai_base_url"] = st.text_input(
        "OPENAI BASE URL",
        key="openai_base_url",
        type="default",
        # Use the current value from st.session_state for the initial value
        value=st.session_state[pagename].get("openai_base_url", ""),
    )

    st.session_state[pagename]["openai_api_key"] = st.text_input(
        "OPENAI API KEY",
        key="openai_api_key",
        type="password",
        value=st.session_state[pagename].get("openai_api_key", ""),
    )

def sidebar_for_selfhost_endpoint(pagename: str):
    
    st.session_state[pagename]["selfhost_model"] = st.sidebar.selectbox(
        "Choose a Self-Host model", ["THUDM/chatglm3-6b-32k"], key="selfhost_model", index=0
    )

    st.session_state[pagename]["selfhost_openai_base_url"] = st.text_input(
        "SelfHost OPENAI BASE URL",
        key="selfhost_openai_base_url",
        type="default",
        # Use the current value from st.session_state for the initial value
        value=st.session_state[pagename].get("selfhost_openai_base_url", ""),
    )

    st.session_state[pagename]["selfhost_openai_api_key"] = st.text_input(
        "SelfHost OPENAI API KEY",
        key="selfhost_openai_api_key",
        type="password",
        value=st.session_state[pagename].get("selfhost_openai_api_key", ""),
    )

def sidebar_for_aoai_endpoint(pagename: str):
    st.session_state[pagename]["azure_openai_endpoint"] = st.text_input(
        "AZURE OPENAI ENDPOINT",
        key="azure_openai_endpoint",
        type="default",
        value=st.session_state[pagename].get("azure_openai_endpoint", ""),
    )

    st.session_state[pagename]["azure_openai_api_key"] = st.text_input(
        "AZURE OPENAI API KEY",
        key="azure_openai_api_key",
        type="password",
        value=st.session_state[pagename].get("azure_openai_api_key", ""),
    )

    st.session_state[pagename]["azure_openai_api_version"] = st.text_input(
        "Azure OPENAI API VERSION",
        key="azure_openai_api_version",
        type="default",
        value=st.session_state[pagename].get("azure_openai_api_version", ""),
    )

    st.session_state[pagename]["azure_openai_model"] = st.text_input(
        "Azure OPENAI MODEL",
        key="azure_openai_model",
        type="default",
        value=st.session_state[pagename].get("azure_openai_model", ""),
    )
