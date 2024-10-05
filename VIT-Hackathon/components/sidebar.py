import streamlit as st

class Sidebar:
    def render(self):
        st.sidebar.header("Menu")
        st.sidebar.button("Home", on_click=lambda: setattr(st.session_state, 'page', 'home'))
        st.sidebar.button("My Profile", on_click=lambda: setattr(st.session_state, 'page', 'My Profile'))
        st.sidebar.button("Dark Mode" if st.session_state.theme == 'light' else "Light Mode",
                          on_click=self.toggle_theme)
        #st.sidebar.button("Logout", on_click=lambda: setattr(st.session_state, 'page', 'logout'))

    def toggle_theme(self):
        st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
