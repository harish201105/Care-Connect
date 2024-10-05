import streamlit as st
import firebase_admin
from firebase_admin import credentials
import json
import requests
import os


class LoginPage:
    def __init__(self):
        # Load Firebase credentials and initialize Firebase Admin SDK
        cred_path = "carering firebase-adminsdk.json"  # Update the path accordingly
        self.cred = credentials.Certificate(cred_path)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(self.cred)  # Initialize only once

        # Initialize session state variables for user credentials and login status
        if 'username' not in st.session_state:
            st.session_state.username = ''
        if 'useremail' not in st.session_state:
            st.session_state.useremail = ''
        if 'is_logged_in' not in st.session_state:
            st.session_state.is_logged_in = False
        if 'email_input' not in st.session_state:
            st.session_state.email_input = ''
        if 'password_input' not in st.session_state:
            st.session_state.password_input = ''
        if 'username_input' not in st.session_state:
            st.session_state.username_input = ''

    def sign_up_with_email_and_password(self, email, password, username=None, return_secure_token=True):
        """Sign up a user using email and password."""
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
        api_key = os.getenv("FIREBASE_API_KEY")  # Get API key from environment variables
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": return_secure_token
        }
        if username:
            payload["displayName"] = username
        payload = json.dumps(payload)
        r = requests.post(rest_api_url, params={"key": api_key}, data=payload)
        if r.ok:
            user_info = r.json()
            st.session_state['current_page'] = 'home'  # Redirect to home on successful signup
            return user_info['email']
        else:
            st.error('Signup failed: ' + r.json().get('error').get('message'))

    def sign_in_with_email_and_password(self, email, password, return_secure_token=True):
        """Sign in a user using email and password."""
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
        api_key = os.getenv("FIREBASE_API_KEY")  # Get API key from environment variables
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": return_secure_token
        }
        payload = json.dumps(payload)
        r = requests.post(rest_api_url, params={"key": api_key}, data=payload)
        if r.ok:
            data = r.json()
            st.session_state.username = data.get('displayName', email.split('@')[0])
            st.session_state.useremail = data['email']
            st.session_state.is_logged_in = True
            st.session_state['current_page'] = 'home'  # Redirect to home on successful login
            return {'email': data['email'], 'username': data.get('displayName')}
        else:
            st.error('Signin failed: ' + r.json().get('error').get('message'))

    def handle_login(self):
        """Handle user login process."""
        userinfo = self.sign_in_with_email_and_password(st.session_state.email_input, st.session_state.password_input)
        if not userinfo:
            st.error('Login Failed')

    def render(self):
        """Build the UI for login and signup."""
        st.title('Welcome to Care Connect')
        if not st.session_state.is_logged_in:
            choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])
            email = st.text_input('Email Address', key='email_input', value=st.session_state.email_input)
            password = st.text_input('Password', type='password', key='password_input', value=st.session_state.password_input)

            if choice == 'Sign up':
                username = st.text_input("Enter your unique username", key='username_input', value=st.session_state.username_input)
                if st.button('Create my account'):
                    self.sign_up_with_email_and_password(email=email, password=password, username=username)
            elif st.button('Login'):
                self.handle_login()
        else:
            st.write(f"Welcome, {st.session_state.username} ({st.session_state.useremail})")
            if st.button('Sign out'):
                st.session_state.is_logged_in = False
                st.session_state['current_page'] = 'login'  # Navigate to login page after sign out
