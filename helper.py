import streamlit as st

def new_chat():
    save = []
    for i in range(len(st.session_state.messages)-1, -1, -1):
        msg = st.session_state.messages[i]
        if msg["content"] != None:            
            save.append(msg["role"] + ": " + msg["content"] + "\n")
        else:
            save.append(msg["role"] + ": " + "No message returned from ChatGPT. Please retry later. \n")  
    
    st.session_state["stored_session"].append(save)
    st.session_state.messages = []
    st.session_state["first_message_in_sesson"] = False

def generate_conversion():    
    save = []
    for i in range(len(st.session_state.messages)):        
        msg = st.session_state.messages[i]        
        if msg["content"] != None:            
            save.append(msg["role"] + ": " + msg["content"] + "\n")
        else:
            save.append(msg["role"] + ": " + "No message returned from ChatGPT. Please retry later. \n")
    download_str = '\n'.join(save)
    return download_str