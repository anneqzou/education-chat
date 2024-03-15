import streamlit as st
from openai import OpenAI
from utils.helper import (
    clear_chat_history,
    format_output,
    initialize_llm_parameters_session_state,
    initialize_page_session_state,
    sidebar_for_llm_parameters,
    sidebar_for_openai_endpoint,
)

pagename = "openai_history"

default_chatbot_values = {
    "messages": [{"role": "assistant", "content": "How can I help you?"}],
    "llm_model": "",
    "openai_base_url": "",
    "openai_api_key": "",
}

initialize_page_session_state(pagename, default_chatbot_values)

initialize_llm_parameters_session_state(pagename)

with st.sidebar:
    st.subheader("Models and parameters")

    st.session_state[pagename]["llm_model"] = st.sidebar.selectbox(
        "Choose the model", ["gpt-3.5-turbo"], key="llm_model", index=0
    )

    sidebar_for_openai_endpoint(pagename)

    sidebar_for_llm_parameters(pagename)

st.sidebar.button("Clear Chat History", on_click=clear_chat_history, args=(pagename,))
st.title("💬 Open AI Chatbot")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")

for msg in st.session_state[pagename]["messages"]:
    if msg["role"] == "assistant":
        st.chat_message(msg["role"]).write(msg["content"])
    else:
        st.chat_message(msg["role"]).code(msg["content"])

if prompt := st.chat_input():
    if not st.session_state[pagename]["openai_base_url"]:
        st.info("Please add your Self Host LLM Endpoint to continue.")
        st.stop()

    if not st.session_state[pagename]["openai_api_key"]:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    if not st.session_state[pagename]["llm_model"]:
        st.info("Please add your SelfHost LLM Model to continue.")
        st.stop()

    client = OpenAI(
        api_key=st.session_state[pagename]["openai_api_key"],
        base_url=st.session_state[pagename]["openai_base_url"],
    )

    with st.chat_message("user"):
        output_string = format_output(prompt)
        st.code(output_string)
        st.session_state[pagename]["messages"].append(
            {"role": "user", "content": prompt}
        )

    if st.session_state[pagename]["stream_mode"] == "No":
        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model=st.session_state[pagename]["llm_model"],
                messages=st.session_state[pagename]["messages"],
                temperature=st.session_state[pagename]["temperature"],
                max_tokens=st.session_state[pagename]["max_tokens"],
                top_p=st.session_state[pagename]["top_p"],
                frequency_penalty=st.session_state[pagename]["frequency_penalty"],
                presence_penalty=st.session_state[pagename]["presence_penalty"],
            )
            msg = response.choices[0].message.content
            st.write(msg)
            st.session_state[pagename]["messages"].append(
                {"role": "assistant", "content": msg}
            )

    else:
        with st.chat_message("assistant"):
            completion = client.chat.completions.create(
                model=st.session_state[pagename]["llm_model"],
                messages=st.session_state[pagename]["messages"],
                temperature=st.session_state[pagename]["temperature"],
                max_tokens=st.session_state[pagename]["max_tokens"],
                top_p=st.session_state[pagename]["top_p"],
                frequency_penalty=st.session_state[pagename]["frequency_penalty"],
                presence_penalty=st.session_state[pagename]["presence_penalty"],
                stream=True,
            )
            response = st.write_stream(completion)
            st.session_state[pagename]["messages"].append(
                {"role": "assistant", "content": response}
            )
