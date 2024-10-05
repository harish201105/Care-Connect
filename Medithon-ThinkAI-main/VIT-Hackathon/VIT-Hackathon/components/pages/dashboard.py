# dashboard.py
import streamlit as st
from components.pages.base_page import Page

class DashboardPage(Page):
    def render(self):
        st.subheader("My Dashboard")
        st.markdown("# Care-Connect: Your post-discharge engagement system", unsafe_allow_html=True)

        # Create a 4-column layout for buttons
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.button("Health Assist", key='health_assist_button', on_click=lambda: setattr(st.session_state, 'page', 'ai_health_assistant'))
        with col2:
            st.button("Health Surfers", key='health_surfers_button', on_click=lambda: setattr(st.session_state, 'page', 'health_surfers'))
        with col3:
            st.button("Physio-Hub", key='physio_hub_button', on_click=lambda: setattr(st.session_state, 'page', 'physio_hub'))
        with col4:
            st.button("Care-Ring", key='care_ring_button', on_click=lambda: setattr(st.session_state, 'page', 'care_ring'))
