import streamlit as st
from AzureGPT_API import CallAzureGPT,CallAzure_GPT35
from helper import new_chat, generate_conversion

# Initialize session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []

if "first_message_in_sesson" not in st.session_state:
    st.session_state["first_message_in_sesson"] = False
# End of Initialize session_state

# Set up sidebar with various options
with st.sidebar.expander("🛠️ ", expanded=False):
    # Option for model
    MODEL = st.selectbox(label='Model', options=['gpt-3.5-turbo','gpt-4'], index=0)

st.title("Education Chatbot")
st.subheader(" Powered by 🦜 Azure GPT + Streamlit")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

with st.container():
    # React to user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        if MODEL == "gpt-4":
            response = CallAzureGPT(prompt)
        elif MODEL == "gpt-3.5-turbo":
            response = CallAzure_GPT35(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state["first_message_in_sesson"] = True

if st.session_state["first_message_in_sesson"] == True:
    st.download_button(label="Download", data=generate_conversion(), key="assistant-download")

# Add a button to start a new chat
st.sidebar.button("New Chat", on_click = new_chat, type='primary')

# Display stored conversation sessions in the sidebar
for i, sublist in enumerate(st.session_state.stored_session):
    with st.sidebar.expander(label= f"Session:{i}"):
        st.write(sublist)