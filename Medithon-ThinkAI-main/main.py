from user_interface.login_page import LoginPage
from user_interface.dash import dash_page  # Make sure this import works
from user_interface.chat_page import ChatPage  # Import the ChatPage class
from user_interface.physio_page import PhysioPage  # Import the PhysioPage class
from user_interface.healthsurfers_page import HealthSurfersPage  # Import the HealthSurfersPage class

import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file

def main():
    # Initialize the current page session state if it doesn't exist
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'login'  # Default page is the login page

    # Navigate based on the current page in session state
    if st.session_state['current_page'] == 'login':
        login_instance = LoginPage()
        login_instance.render()
    elif st.session_state['current_page'] == 'home':
        dash_page()
    elif st.session_state['current_page'] == 'chatbot':
        chat_instance = ChatPage()
        chat_instance.render()  # Render the chat page
    elif st.session_state['current_page'] == 'physio':
        physio_instance = PhysioPage()
        physio_instance.render()
    elif st.session_state['current_page'] == 'healthsurfers':
        healthsurfers_instance = HealthSurfersPage()
        healthsurfers_instance.render()

if __name__ == '__main__':
    st.set_page_config(page_title='Care Connect', layout='wide')
    main()
