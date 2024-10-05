# login_page.py
import streamlit as st
import requests
import json
import os

class LoginPage:
    def __init__(self, navigate_home, navigate_signup):  # Ensure both parameters are accepted
        self.navigate_home = navigate_home
        self.navigate_signup = navigate_signup  # Store the signup navigation method

    def sign_in_with_email_and_password(self, email, password):
        """Sign in a user using email and password."""
        api_key = os.getenv("FIREBASE_API_KEY")  # Get API key from .env
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
        payload = json.dumps({
            "email": email,
            "password": password,
            "returnSecureToken": True
        })
        response = requests.post(rest_api_url, params={"key": api_key}, data=payload)
        return response

    def handle_login(self, email, password):
        """Process login and handle UI redirection."""
        response = self.sign_in_with_email_and_password(email, password)
        if response.ok:
            data = response.json()
            st.session_state.username = data.get('displayName', email.split('@')[0])
            st.session_state.useremail = data['email']
            st.session_state.is_logged_in = True
            self.navigate_home()
        else:
            st.error('Signin failed: ' + response.json().get('error', {}).get('message', 'An error occurred'))

    def render(self):
        """UI for login."""
        st.title('Login to Care-Connect')
        email = st.text_input('Email Address', key='login_email')
        password = st.text_input('Password', type='password', key='login_password')
        if st.button('Login'):
            self.handle_login(email, password)
        
        # Add a link/button to navigate to the signup page
        st.markdown("---")
        st.write("Don't have an account?")
        if st.button("Sign up", key='signup_button'):
            self.navigate_signup()  # Navigate to signup page
