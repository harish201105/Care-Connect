import streamlit as st

class Layout:
    def __init__(self):
        self.light_theme = """
        <style>
        body { background-color: white; color: black; }
        .css-1d391kg { padding: 0.25rem 1rem; }
        button { margin: 5px; border: 2px solid; border-radius: 10px; font-weight: bold; color: black; }
        h1 { font-size: 2.5em; color: black; }
        </style>
        """
        self.dark_theme = """
        <style>
        body { background-color: #333; color: white; }
        .css-1d391kg { padding: 0.25rem 1rem; }
        button { margin: 5px; border: 2px solid; border-radius: 10px; font-weight: bold; color: white; }
        h1 { font-size: 2.5em; color: white; }
        </style>
        """

    def apply_theme(self):
        if st.session_state.theme == 'light':
            st.markdown(self.light_theme, unsafe_allow_html=True)
        else:
            st.markdown(self.dark_theme, unsafe_allow_html=True)
