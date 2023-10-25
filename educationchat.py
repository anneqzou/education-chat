import streamlit as st
import urllib.request
import json
import os
import ssl
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

def CallAzureGPT(input):
    # Allow self-signed certificate
    allowSelfSignedHttps(True)

    # Azure Key Vault details
    key_vault_uri = "https://education-chat-access.vault.azure.net/"
    secret_name = "V1d8Q~vFI2HG_tfWY0CEh7I4v33xfw0MB5eE.aCc"

    # Get credentials
    credential = DefaultAzureCredential()

    # Create a secret client using the default credential
    secret_client = SecretClient(vault_url=key_vault_uri, credential=credential)

    # Retrieve the secret
    retrieved_secret = secret_client.get_secret(secret_name)

    # Use the secret (API Key) to call the REST API
    api_key = retrieved_secret.value

    data = {"question": input}
    body = str.encode(json.dumps(data))
    
    url = 'https://rai-aml-usw-fpxsc.westus.inference.ml.azure.com/score'

    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'rai-aml-usw-fpxsc-1' }

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        json_obj = json.loads(result)
        answer = json_obj.get("answer")
        print(answer)
        return answer
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())

# Define function to start a new chat
def new_chat():
    """
    Clears session state and starts a new chat.
    """
    save = []
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        save.append("User:" + st.session_state["past"][i])
        save.append("Bot:" + st.session_state["generated"][i])        
    st.session_state["stored_session"].append(save)
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["input"] = ""
    st.session_state.entity_memory.entity_store = {}
    st.session_state.entity_memory.buffer.clear()

class EntityMemory:
    def __init__(self):
        self.entity_store = {}
        self.buffer = []

    def add_entity(self, entity, value):
        self.entity_store[entity] = value

    def get_entity(self, entity):
        return self.entity_store.get(entity)

    def add_to_buffer(self, message):
        self.buffer.append(message)

    def clear_buffer(self):
        self.buffer.clear()

# Initialize session states
if 'key' not in st.session_state:
    st.session_state['key'] = 'value'
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""
if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "entity_memory" not in st.session_state:
    st.session_state.entity_memory = EntityMemory()
if "entity_store" not in st.session_state:
    st.session_state.entity_store = {}
if "buffer" not in st.session_state:
    st.session_state.buffer = []

st.title("Education Chatbot")
st.subheader(" Powered by 🦜 Azure GPT + Streamlit")

# Define function to get user input
def get_text():
    """
    Get the user input text.

    Returns:
        (str): The text entered by the user
    """
    input_text = st.text_input("You: ", st.session_state["input"], key="input",
                            placeholder="Your AI assistant here! Ask me anything ...", 
                            label_visibility='hidden')
    return input_text

#for message in st.session_state.messages:
    #with st.chat_message(message["role"]):
     #   st.markdown(message["content"])

#if prompt := st.chat_input("What is up?"):
    #st.session_state.messages.append({"role": "user", "content": prompt})
    #with st.chat_message("user"):
     #   st.markdown(prompt)

    #with st.chat_message("assistant"):
     #   message_placeholder = st.empty()
     #   full_response = CallAzureGPT(prompt)        
     #   message_placeholder.markdown(full_response)
     #   st.session_state.messages.append({"role": "assistant", "content": full_response})

# Get the user input
user_input = get_text()

# Generate the output using the ConversationChain object and the user input, and add the input/output to the session
if user_input:
    full_response = CallAzureGPT(input=user_input)  
    st.session_state.past.append(user_input)  
    st.session_state.generated.append(full_response)  

# Add a button to start a new chat
st.sidebar.button("New Chat", on_click = new_chat, type='primary')

# Allow to download as well
download_str = []
# Display the conversation history using an expander, and allow the user to download it
with st.expander("Conversation", expanded=True):
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        st.info(st.session_state["past"][i],icon="🧐")
        st.success(st.session_state["generated"][i], icon="🤖")
        download_str.append(st.session_state["past"][i])
        download_str.append(st.session_state["generated"][i])
    
    # Can throw error - requires fix
    download_str = '\n'.join(download_str)
    if download_str:
        st.download_button('Download',download_str)

# Display stored conversation sessions in the sidebar
for i, sublist in enumerate(st.session_state.stored_session):
        with st.sidebar.expander(label= f"Conversation-Session:{i}"):
            st.write(sublist)

# Allow the user to clear all stored conversation sessions
if st.session_state.stored_session:   
    if st.sidebar.checkbox("Clear-all"):
        del st.session_state.stored_session