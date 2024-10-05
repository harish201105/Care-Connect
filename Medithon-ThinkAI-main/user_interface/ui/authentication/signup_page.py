# signup_page.py
import streamlit as st
import requests
import json
import os

class SignupPage:
    def __init__(self, navigate_home):
        self.navigate_home = navigate_home

    def sign_up_with_email_and_password(self, email, password, username):
        """Sign up a user using email and password."""
        api_key = os.getenv("FIREBASE_API_KEY")  # Get API key from .env
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
        payload = json.dumps({
            "email": email,
            "password": password,
            "displayName": username,
            "returnSecureToken": True
        })
        response = requests.post(rest_api_url, params={"key": api_key}, data=payload)
        return response

    def handle_signup(self, email, password, username):
        """Process signup and handle UI redirection."""
        response = self.sign_up_with_email_and_password(email, password, username)
        if response.ok:
            st.session_state.is_logged_in = True
            self.navigate_home()
        else:
            st.error('Signup failed: ' + response.json().get('error', {}).get('message', 'An error occurred'))

    def render(self):
        """UI for signup."""
        st.title('Create Account on Care-Connect')
        email = st.text_input('Email Address', key='signup_email')
        password = st.text_input('Password', type='password', key='signup_password')
        username = st.text_input('Username', key='signup_username')
        if st.button('Create my account'):
            self.handle_signup(email, password, username)
