import streamlit as st


def initialize_page_config():
    st.set_page_config(
        page_title="LLMGateway Test Center - powered by Streamlit",
        page_icon=":guardsman:",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def main():
    # Initialize page config
    initialize_page_config()

    # Add welcome message
    st.write("# Welcome to LLMGateway Test Center!")

    st.write("## Select chatbot to test:")

    if st.button("OpenAI Chatbot"):
        st.switch_page("chatbot/pages/1_OpenAI_Chatbot.py")

    if st.button("AOAI Chatbot"):
        st.switch_page("chatbot/pages/2_AOAI_Chatbot.py")

    if st.button("Self Host Chatbot"):
        st.switch_page("chatbot/pages/3_SelfHost_Chatbot.py")


if __name__ == "__main__":
    main()
