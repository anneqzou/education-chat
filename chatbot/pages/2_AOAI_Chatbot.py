import streamlit as st
from openai import AzureOpenAI
from utils.helper import (
    clear_chat_history,
    format_output,
    initialize_llm_parameters_session_state,
    initialize_page_session_state,
    sidebar_for_aoai_endpoint,
    sidebar_for_llm_parameters,
)

pagename = "aoai_history"

default_chatbot_values = {
    "messages": [{"role": "assistant", "content": "How can I help you?"}],
    "azure_openai_endpoint": "",
    "azure_openai_api_key": "",
    "azure_openai_api_version": "",
    "azure_openai_model": "",
}

initialize_page_session_state(pagename, default_chatbot_values)

initialize_llm_parameters_session_state(pagename)

with st.sidebar:

    st.subheader("Models and parameters")

    sidebar_for_aoai_endpoint(pagename)

    sidebar_for_llm_parameters(pagename)

st.sidebar.button("Clear Chat History", on_click=clear_chat_history, args=(pagename,))

st.title("💬 Azure OpenAI Chatbot")
st.caption("🚀 A streamlit chatbot powered by AOAI LLM")

for msg in st.session_state[pagename]["messages"]:
    st.chat_message(msg["role"]).code(msg["content"])

if prompt := st.chat_input():
    if not st.session_state[pagename]["azure_openai_endpoint"]:
        st.info("Please add your Azure OpenAI Endpoint to continue.")
        st.stop()

    if not st.session_state[pagename]["azure_openai_api_key"]:
        st.info("Please add your Azure OpenAI API key to continue.")
        st.stop()

    if not st.session_state[pagename]["azure_openai_api_version"]:
        st.info("Please add your Azure OpenAI API Version to continue.")
        st.stop()

    if not st.session_state[pagename]["azure_openai_model"]:
        st.info("Please add your Azure OpenAI Model to continue.")
        st.stop()

    client = AzureOpenAI(
        api_key=st.session_state[pagename]["azure_openai_api_key"],
        azure_endpoint=st.session_state[pagename]["azure_openai_endpoint"],
        api_version=st.session_state[pagename]["azure_openai_api_version"],
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
                model=st.session_state[pagename]["azure_openai_model"],
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
                model=st.session_state[pagename]["azure_openai_model"],
                messages=st.session_state[pagename]["messages"],
                temperature=st.session_state[pagename]["temperature"],
                max_tokens=st.session_state[pagename]["max_tokens"],
                top_p=st.session_state[pagename]["top_p"],
                frequency_penalty=st.session_state[pagename]["frequency_penalty"],
                presence_penalty=st.session_state[pagename]["presence_penalty"],
                stream=True,
            )

            # AOAI will return empty content for the first few chunks, it may throw exception with below line
            response = st.write_stream(completion)
            st.session_state[pagename]["messages"].append(
                {"role": "assistant", "content": response}
            )
