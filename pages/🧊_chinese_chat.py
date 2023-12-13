import streamlit as st
from utils.AzureGPT_API import CallAzure_Llama2
from utils.chinese_chat_buildin_prompt import buildInPrompts

def initialize_page_config():
    """
    Initializes the page configuration for the Streamlit app.

    The function sets the page title, icon, layout, and initial sidebar state.

    Returns:
        None
    """
    st.set_page_config(        
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize session_state
    if "messages_chinese_chatbot" not in st.session_state:
        st.session_state.messages_chinese_chatbot = []

    if "stored_session_chinese_chatbot" not in st.session_state:
        st.session_state.stored_session_chinese_chatbot = []

    if "first_message_in_sesson_chinese_chatbot" not in st.session_state:
        st.session_state.first_message_in_sesson_chinese_chatbot = False

    if "trigger_by_built_in_prompt_chinese_chatbot" not in st.session_state:
        st.session_state.trigger_by_built_in_prompt_chinese_chatbot = False
    # End of Initialize session_state

def new_chat():
    save = []
    for i in range(len(st.session_state.messages_chinese_chatbot)-1, -1, -1):
        msg = st.session_state.messages_chinese_chatbot[i]
        if msg["content"] != None:            
            save.append(msg["role"] + ": " + msg["content"] + "\n")
        else:
            save.append(msg["role"] + ": " + "No message returned from ChatGPT. Please retry later. \n")  
    
    st.session_state.stored_session_chinese_chatbot.append(save)
    st.session_state.messages_chinese_chatbot = []
    st.session_state.first_message_in_sesson_chinese_chatbot = False

def generate_conversion():    
    save = []
    for i in range(len(st.session_state.messages_chinese_chatbot)):        
        msg = st.session_state.messages_chinese_chatbot[i]        
        if msg["content"] != None:            
            save.append(msg["role"] + ": " + msg["content"] + "\n")
        else:
            save.append(msg["role"] + ": " + "No message returned from ChatGPT. Please retry later. \n")
    download_str = '\n'.join(save)
    return download_str

# Initialize page config
initialize_page_config()

# Set up sidebar with various options
with st.sidebar:
    # Option for model
    MODEL = st.radio(
        "Select Model You Want To Use",
        ["llama2"]
    )
    if MODEL == 'llama2':
        st.write('You selected llama2.')

st.title("Chinese Chat")
st.subheader(" Powered by 🦜 PromptFlow + LLAMA2 + Streamlit")

def send_button_ques(prompt):
    with st.container():
        # Display user message in chat message container
        st.session_state.trigger_by_built_in_prompt_chinese_chatbot = True
        # Add user message to chat history
        st.session_state.messages_chinese_chatbot.append({"role": "user", "content": prompt})
        if MODEL == "llama2":
            response = CallAzure_Llama2(prompt)
        # Add assistant response to chat history
        st.session_state.messages_chinese_chatbot.append({"role": "assistant", "content": response})
        if st.session_state.first_message_in_sesson_chinese_chatbot == False:
            st.session_state.first_message_in_sesson_chinese_chatbot = True

# Render suggested question buttons
buttons = st.container()
for q in buildInPrompts:
    button_ques = buttons.button(
        label=q["title"], 
        on_click=send_button_ques, 
        args=[q["prompt"]] 
    )


# React to user input
if prompt := st.chat_input("What is up?"):
    st.session_state.trigger_by_built_in_prompt_chinese_chatbot = False
    # Display user message in chat message container
    # Add user message to chat history
    st.session_state.messages_chinese_chatbot.append({"role": "user", "content": prompt})

    if MODEL == "llama2":
        response = CallAzure_Llama2(prompt)

    # Display assistant response in chat message container
    # Add assistant response to chat history
    st.session_state.messages_chinese_chatbot.append({"role": "assistant", "content": response})
    st.session_state.first_message_in_sesson_chinese_chatbot = True

# Display chat messages from history on app rerun
for message in st.session_state.messages_chinese_chatbot:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.first_message_in_sesson_chinese_chatbot == True:
    st.download_button(label="Download", data=generate_conversion(), key="assistant-download")

# Add a button to start a new chat
st.sidebar.button("New Chat", on_click=new_chat, type='primary')

# Display stored conversation sessions in the sidebar
for i, sublist in enumerate(st.session_state.stored_session_chinese_chatbot):
    with st.sidebar.expander(label=f"Session:{i}"):
        st.write(sublist)