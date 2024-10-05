import streamlit as st
from components.layout import Layout
from components.sidebar import Sidebar
from components.pages.pages import Pages
from authentication.login_page import LoginPage
from authentication.signup_page import SignupPage
from components.footer import Footer
from utils.helpers import init_session_state
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Ensure session state is initialized
init_session_state()

# Create instances for Layout, Pages, LoginPage, SignupPage, and Footer
layout = Layout()
pages = Pages()
footer = Footer()
login_page = LoginPage(navigate_home=lambda: setattr(st.session_state, 'current_page', 'home'),
                       navigate_signup=lambda: setattr(st.session_state, 'current_page', 'signup'))
signup_page = SignupPage(navigate_home=lambda: setattr(st.session_state, 'current_page', 'home'))

# Apply the theme
layout.apply_theme()

# Main rendering logic based on the session state 'current_page'
if st.session_state['current_page'] == 'login':
    login_page.render()  # Render login page
elif st.session_state['current_page'] == 'signup':
    signup_page.render()  # Render signup page
else:
    # Render the sidebar and pages only if the user is logged in
    if st.session_state.is_logged_in:
        sidebar = Sidebar()  # Only create Sidebar instance here
        sidebar.render()  # Render sidebar only when logged in

        pages.render()  # Render main pages after logging in

        # Logout button, only visible if logged in

        if st.sidebar.button('Logout', key='sidebar_logout_button'):
            st.session_state.is_logged_in = False
            st.session_state.username = ''
            st.session_state.useremail = ''
            st.session_state['current_page'] = 'login'  # Redirect to login after logout

# Footer rendering
footer.render()
