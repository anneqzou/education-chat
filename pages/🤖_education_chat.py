import streamlit as st
from utils.AzureGPT_API import CallAzureGPT, CallAzure_GPT35
from utils.helper import new_chat, generate_conversion
from utils.education_chat_buildin_prompt import buildInPrompts
import csv

def initialize_page_config():
    """
    Initializes the page configuration for the Streamlit app.

    The function sets the page title, icon, layout, and initial sidebar state.

    Returns:
        None
    """
    st.set_page_config(        
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize session_state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "stored_session" not in st.session_state:
        st.session_state["stored_session"] = []

    if "first_message_in_sesson" not in st.session_state:
        st.session_state["first_message_in_sesson"] = False

    if "trigger_by_built_in_prompt" not in st.session_state:
        st.session_state["trigger_by_built_in_prompt"] = False
    # End of Initialize session_state

# Initialize page config
initialize_page_config()

# Set up sidebar with various options
with st.sidebar:
    # Option for model
    MODEL = st.radio(
        "Select Model You Want To Use",
        ["gpt-4", "gpt-3.5-turbo"]
    )
    if MODEL == 'gpt-3.5-turbo':
        st.write('You selected gpt-3.5-turbo.')
    else:
        st.write("You selected gpt-4")

st.title("Education Chat")
st.subheader(" Powered by 🦜 PromptFlow + Azure GPT + Streamlit")

def send_button_ques(prompt):
    with st.container():
        # Display user message in chat message container
        st.session_state["trigger_by_built_in_prompt"] = True
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        if MODEL == "gpt-4":
            response = CallAzureGPT(prompt)
            #add function to log prompt and response
            log_input_and_response_in_csv_file(prompt, response)
        elif MODEL == "gpt-3.5-turbo":
            response = CallAzure_GPT35(prompt)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        if st.session_state["first_message_in_sesson"] == False:
            st.session_state["first_message_in_sesson"] = True

# Render suggested question buttons
buttons = st.container()
for q in buildInPrompts:
    button_ques = buttons.button(
        label=q["title"], 
        on_click=send_button_ques, 
        args=[q["prompt"]] 
    )

def log_input_and_response_in_csv_file(prompt, response):  
    print("log_input_and_response_in_csv_file")
    with open('log.csv', 'a') as file:
        # when I write to the file, there is comma and new lines in both prompt and response, it will break the csv file. we should consider how to handle this case.
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([prompt, response])


# React to user input
if prompt := st.chat_input("What is up?"):
    st.session_state["trigger_by_built_in_prompt"] = False
    # Display user message in chat message container
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    if MODEL == "gpt-4":
        response = CallAzureGPT(prompt)
        #add function to log prompt and response
        log_input_and_response_in_csv_file(prompt, response)
    elif MODEL == "gpt-3.5-turbo":
        response = CallAzure_GPT35(prompt)

    # Display assistant response in chat message container
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state["first_message_in_sesson"] = True

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state["first_message_in_sesson"] == True:
    st.download_button(label="Download", data=generate_conversion(), key="assistant-download")

# Add a button to start a new chat
st.sidebar.button("New Chat", on_click=new_chat, type='primary')

# Display stored conversation sessions in the sidebar
for i, sublist in enumerate(st.session_state.stored_session):
    with st.sidebar.expander(label=f"Session:{i}"):
        st.write(sublist)