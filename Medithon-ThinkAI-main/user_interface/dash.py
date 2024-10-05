import streamlit as st

def dash_page():
    # Create a two-column layout
    col1, col2 = st.columns([9, 1])  # Adjust the ratio to make the button appear on the right

    with col1:
        # Display the main title at the top left
        st.title("Care Connect")

    with col2:
        # Create a button at the top right side of the page
        if st.button('User'):
            st.session_state['current_page'] = 'user'  # Set session state to navigate to user page

    # Home Page Content
    st.write("Welcome to Care Connect")

    # Redirect to Chatbot
    if st.button('Chatbot'):
        st.session_state['current_page'] = 'chatbot'  # Set session state to navigate to chatbot page

    if st.button('Physio'):
        st.session_state['current_page'] = 'physio'

    if st.button('Health Surfers'):
        st.session_state['current_page'] = 'healthsurfers'
