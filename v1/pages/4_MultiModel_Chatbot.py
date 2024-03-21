import streamlit as st
from openai import AzureOpenAI, OpenAI

from utils.helper import (
    clear_chat_multi_history,
    format_output,
    initialize_llm_parameters_session_state,
    initialize_page_session_state,
    sidebar_for_llm_parameters,
    sidebar_for_openai_endpoint,
    sidebar_for_selfhost_endpoint,
    sidebar_for_aoai_endpoint
)

pagename = "multimodel_history"

default_chatbot_values = {
    "messages": [
    ],
}

initialize_page_session_state(pagename, default_chatbot_values)

initialize_llm_parameters_session_state(pagename)

models = {
    "OpenAI": [],
    "AOAI":  [],
    "SelfHost": [],
}

with st.sidebar:
    selected_models = st.sidebar.multiselect("Select models to compare:", options=list(models.keys()))

    for model in selected_models:
        if model == "OpenAI":
            st.subheader("OpenAI Model:")
            sidebar_for_openai_endpoint(pagename)
        elif model == "AOAI":
            st.subheader("AOAI Model:")
            sidebar_for_aoai_endpoint(pagename)
        elif model == "SelfHost":
            st.subheader("SelfHost Model:")
            sidebar_for_selfhost_endpoint(pagename)

    if selected_models:
        st.subheader("LLM parameters:")
        sidebar_for_llm_parameters(pagename)

st.sidebar.button("Clear Chat History", on_click=clear_chat_multi_history, args=(pagename,))

st.title("💬 Multiple LLM Chatbot")
st.caption("🚀 A streamlit chatbot powered by OpenAI, AOAI and SelfHost LLM")

no_user_msg = True
index = 0
while index < len(st.session_state[pagename]["messages"]):
    if st.session_state[pagename]["messages"][index]["role"] == "user":
        msg = st.session_state[pagename]["messages"][index]
        no_user_msg = False
        st.chat_message(msg["role"]).code(msg["content"])
        index +=1
    else:
        if no_user_msg == True:
            index += 1
            continue
        
        assistant_msg = []

        n = index
        for index2, value in enumerate(st.session_state[pagename]["messages"][n:], start=n):  # Indexing starts at 1
            index = index2 
            if value["role"] == "assistant" and "model" in value:
                assistant_msg.append(value)
                index = index2 + 1
            elif value["role"] == "user":
                index = index2
                break

        cols = st.columns(len(selected_models))
        for idx, model in enumerate(selected_models):
            with cols[idx]:
                # Using list comprehension to find all matches
                matches = [item for item in assistant_msg if item["model"] == model]  # Change "AOAI" to "OpenAI" for an actual match
                response = matches[0]["content"]
                with st.chat_message("assistant"):
                    st.markdown(response)

if prompt := st.chat_input():
    with st.chat_message("user"):
        output_string = format_output(prompt)
        st.code(output_string)
        st.session_state[pagename]["messages"].append(
            {"role": "user", "content": output_string}
        )

    if selected_models:
        cols = st.columns(len(selected_models))
        for idx, model in enumerate(selected_models):
            with cols[idx]:
                st.subheader(f"{model} Chatbot")
                if model == "OpenAI":
                    if not st.session_state[pagename]["openai_base_url"]:
                        st.info("Please add your Self Host LLM Endpoint to continue.")
                        st.stop()

                    if not st.session_state[pagename]["openai_api_key"]:
                        st.info("Please add your OpenAI API key to continue.")
                        st.stop()

                    if not st.session_state[pagename]["openai_model"]:
                        st.info("Please add your SelfHost LLM Model to continue.")
                        st.stop()

                    client = OpenAI(
                        api_key=st.session_state[pagename]["openai_api_key"],
                        base_url=st.session_state[pagename]["openai_base_url"],
                    )
                    
                    modelName = st.session_state[pagename]["openai_model"]

                    organized_messages = []
                    
                    all_messages = st.session_state[pagename]["messages"]
                    for msg in all_messages:
                        if msg["role"] == "user":
                            organized_messages.append(msg)
                        elif msg["role"] == "assistant" and msg["model"] == model:
                            organized_messages.append({"role": "assistant", "content": msg["content"]})

                elif model == "AOAI":
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

                    modelName = st.session_state[pagename]["azure_openai_model"]

                    organized_messages = []
                    
                    all_messages = st.session_state[pagename]["messages"]
                    for msg in all_messages:
                        if msg["role"] == "user":
                            organized_messages.append(msg)
                        elif msg["role"] == "assistant" and msg["model"] == model:
                            organized_messages.append({"role": "assistant", "content": msg["content"]})

                elif model == "SelfHost":
                    if not st.session_state[pagename]["selfhost_openai_base_url"]:
                        st.info("Please add your Self Host LLM Endpoint to continue.")
                        st.stop()

                    if not st.session_state[pagename]["selfhost_openai_api_key"]:
                        st.info("Please add your OpenAI API key to continue.")
                        st.stop()

                    if not st.session_state[pagename]["selfhost_model"]:
                        st.info("Please add your SelfHost LLM Model to continue.")
                        st.stop()

                    client = OpenAI(
                        api_key=st.session_state[pagename]["selfhost_openai_api_key"],
                        base_url=st.session_state[pagename]["selfhost_openai_base_url"],
                    )

                    modelName = st.session_state[pagename]["selfhost_model"]

                    organized_messages = []

                    all_messages = st.session_state[pagename]["messages"]
                    for msg in all_messages:
                        if msg["role"] == "user":
                            organized_messages.append(msg)
                        elif msg["role"] == "assistant" and msg["model"] == model:
                            organized_messages.append({"role": "assistant", "content": msg["content"]})

                with st.chat_message("assistant"):
                    response = client.chat.completions.create(
                        model=modelName,
                        messages=organized_messages,
                        temperature=st.session_state[pagename]["temperature"],
                        max_tokens=st.session_state[pagename]["max_tokens"],
                        top_p=st.session_state[pagename]["top_p"],
                        frequency_penalty=st.session_state[pagename]["frequency_penalty"],
                        presence_penalty=st.session_state[pagename]["presence_penalty"],
                    )

                    msg = response.choices[0].message.content

                    st.markdown(msg)
                    st.session_state[pagename]["messages"].append(
                        {"role": "assistant", "model": model, "content": msg}
                    )

