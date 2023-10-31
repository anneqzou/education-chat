# BEGIN: jk4d9f8d3k2
import streamlit as st

def initialize_page_config():
    """
    Initializes the page configuration for the Streamlit app.

    The function sets the page title, icon, layout, and initial sidebar state.

    Returns:
        None
    """
    st.set_page_config(
        page_title="LLM App - powered by PromptFLow and Streamlit",
        page_icon=":guardsman:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def main():
    # Initialize page config    
    initialize_page_config()

    # Add welcome message
    st.write("# Welcome to the LLM Toolbox!")
    st.write("This website provides two chat bots to help you learn and practice languages.")

    # Introduce education chat bot
    st.write("## Education Chat")
    st.write("The Education Chat is designed to help you learn and practice English. It can answer questions about grammar, vocabulary, and more. Give it a try!")

    # Introduce Chinese chat bot
    st.write("## Chinese Chat")
    st.write("The Chinese Chat is designed to talk with you in Chinese. Give it a try!")
    
if __name__ == "__main__":
    main()