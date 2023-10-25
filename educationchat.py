import streamlit as st
import urllib.request
import json
import os
import ssl
from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential



def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

def CallAzureGPT(input):
    # Allow self-signed certificate
    allowSelfSignedHttps(True)

    # Azure Key Vault and Secret Client Setup    
    key_vault_uri = st.secrets["AZURE_KEY_VAULT_URI"]
    credential = ClientSecretCredential(
        client_id=st.secrets["AZURE_CLIENT_ID"],
        tenant_id=st.secrets["AZURE_TENANT_ID"],
        client_secret=st.secrets["AZURE_CLIENT_SECRET"]
    )

    # Create a secret client using the default credential
    secret_client = SecretClient(vault_url=key_vault_uri, credential=credential)

    # Retrieve the secret and Use the secret (API Key) to call the REST API
    retrieved_secret = secret_client.get_secret(st.secrets["AZURE_SECRET_NAME"])
    AML_API_key = retrieved_secret.value

    # Define the request data
    body = str.encode(json.dumps({"question": input}))
    AML_Deployment_Endpoint = st.secrets["AZURE_ML_ENDPOINT"]
    AML_Deployment_Name = st.secrets["AZURE_ML_Name"]
    headers = {
        'Content-Type':'application/json', 
        'Authorization':('Bearer '+ AML_API_key), 
        'azureml-model-deployment': AML_Deployment_Name
    }

    req = urllib.request.Request(AML_Deployment_Endpoint, body, headers)

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