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
        #print(answer)
        return answer
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())

def CallAzure_GPT35(input):
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
    retrieved_secret = secret_client.get_secret(st.secrets["AZURE_SECRET_NAME_GPT35"])
    AML_API_key = retrieved_secret.value

    # Define the request data
    body = str.encode(json.dumps({"question": input}))
    AML_Deployment_Endpoint = st.secrets["AZURE_ML_ENDPOINT_GPT35"]
    AML_Deployment_Name = st.secrets["AZURE_ML_Name_GPT35"]
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
        #print(answer)
        return answer
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())