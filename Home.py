import streamlit as st
from openai import AzureOpenAI, OpenAI

from utils.helper import (
    initialize_page_config,
    initialize_page_session_state,
    initialize_llm_default_parameters_session_state,
    clear_chat_multi_history,
    sidebar_for_llm_endpoint,
    sidebar_for_llm_parameters,
    check_required_parameter,
    format_output,
    llm_models
)

initialize_page_config()
initialize_page_session_state()
initialize_llm_default_parameters_session_state()

with st.sidebar:
    st.header("Select LLMs:")
    for llm in llm_models.keys():
        selected_llm = st.checkbox(label=f"{llm}", key=f"selected_{llm}")
        if selected_llm:
            sidebar_for_llm_endpoint(llm)
            selected_models = st.sidebar.multiselect("select models:", options=list(llm_models[llm]), key=f"selected_{llm}_models",default=llm_models[llm][0:1])
            for model in selected_models:
                st.caption(f"Parameters for {llm} {model}")
                sidebar_for_llm_parameters(llm, model)

st.sidebar.button("Clear Chat History", on_click=clear_chat_multi_history)

st.title("💬 Chatbot with multiple LLMs")
st.caption("🚀 A streamlit chatbot powered by OpenAI, AOAI and SelfHost LLM. Run multiple LLMs in parallel and compare the results.")

total_columns = 0
for llm in llm_models.keys():
    selected_llm = st.session_state[f"selected_{llm}"]
    if selected_llm:
        supported_models = llm_models[llm]
        for model in st.session_state[f"selected_{llm}_models"]:
            if model in supported_models:
                total_columns += 1

all_model_messages = []
llm_models_name = []
for llm in llm_models.keys():
    selected_llm = st.session_state[f"selected_{llm}"]
    if selected_llm:   
        for model in st.session_state[f"selected_{llm}_models"]:
            if model not in llm_models[llm]:
                continue
            all_model_messages.append(st.session_state[llm][model]["messages"])
            llm_models_name.append(f"{llm} {model}")

user_messages = []
if all_model_messages != []:
    user_messages = [msg for msg in all_model_messages[0] if msg['role'] == 'user']

for user_message in user_messages:
    st.chat_message("user").code(user_message["content"])
    cols = st.columns(len(all_model_messages))

    for i, model_messages in enumerate(all_model_messages):
        # Find the assistant response that corresponds to the current user question
        response = next((msg['content'] for msg in model_messages if msg['role'] == 'assistant' and 
                         model_messages.index(msg) == all_model_messages[0].index(user_message) + 1), "No response")
        with cols[i]:
            st.caption(llm_models_name[i])
            st.chat_message("assistant").write(response)

default_headers = {
    "x-lg-quota-identity": "LLMGateway:Apps:Chatbot",
    "x-lg-quota-priority": "2"
}

if prompt := st.chat_input():
    with st.chat_message("user"):
        output_string = format_output(prompt)
        st.code(output_string)

    cols = st.columns(total_columns)
    idx = 0
    for llm in llm_models.keys():
        selected_llm = st.session_state[f"selected_{llm}"]
        if selected_llm:            
            check_required_parameter(llm)
            if llm == "AOAI":
                client = AzureOpenAI(
                    api_key=st.session_state[llm]["api_key"],
                    azure_endpoint=st.session_state[llm]["base_url"],
                    api_version=st.session_state[llm]["api_version"],
                    default_headers=default_headers
                )
            else:
                client = OpenAI(
                    api_key=st.session_state[llm]["api_key"],
                    base_url=st.session_state[llm]["base_url"],
                    default_headers=default_headers
                )

            with cols[idx]:
                for model in st.session_state[f"selected_{llm}_models"]:
                    if model not in llm_models[llm]:
                        continue

                    st.caption(f"{llm} {model}")
                    
                    # Add user messages to the chat history
                    st.session_state[llm][model]["messages"].append(
                            {"role": "user", "content": output_string}
                    )

                    with st.chat_message("assistant"):

                        if st.session_state[llm][model]["stream_mode"] == "No":
                            response = client.chat.completions.create(
                                model=model,
                                messages=st.session_state[llm][model]["messages"],
                                temperature=st.session_state[llm][model]["temperature"],
                                max_tokens=st.session_state[llm][model]["max_tokens"],
                                top_p=st.session_state[llm][model]["top_p"],
                                frequency_penalty=st.session_state[llm][model]["frequency_penalty"],
                                presence_penalty=st.session_state[llm][model]["presence_penalty"],
                            )

                            msg = response.choices[0].message.content
                            st.markdown(msg)

                            st.session_state[llm][model]["messages"].append(
                                {"role": "assistant", "content": msg}
                            )
                        else:
                            response = client.chat.completions.create(
                                model=model,
                                messages=st.session_state[llm][model]["messages"],
                                temperature=st.session_state[llm][model]["temperature"],
                                max_tokens=st.session_state[llm][model]["max_tokens"],
                                top_p=st.session_state[llm][model]["top_p"],
                                frequency_penalty=st.session_state[llm][model]["frequency_penalty"],
                                presence_penalty=st.session_state[llm][model]["presence_penalty"],
                                stream=True,
                            )

                            msg = st.write_stream(response)
                            st.session_state[llm][model]["messages"].append(
                                {"role": "assistant", "content": msg}
                            )
                    
                    idx += 1