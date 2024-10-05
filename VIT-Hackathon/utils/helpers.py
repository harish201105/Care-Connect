import streamlit as st

def init_session_state():
    """Initialize session state variables with default values."""
    
    # Initialize the current page state (login by default)
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'login'  # Default to 'login' page

    # Initialize the page for internal page navigation (My Profile, home, etc.)
    if 'page' not in st.session_state:
        st.session_state.page = 'home'  # Default to 'home'

    # Initialize the theme (default to 'light')
    if 'theme' not in st.session_state:
        st.session_state['theme'] = 'light'  # Default theme is 'light'

    # Initialize login state (default to False, meaning user is not logged in)
    if 'is_logged_in' not in st.session_state:
        st.session_state['is_logged_in'] = False

    # Initialize the username and email for the session
    if 'username' not in st.session_state:
        st.session_state['username'] = ''

    if 'useremail' not in st.session_state:
        st.session_state['useremail'] = ''

    # Any other session state variables can be added here as needed
