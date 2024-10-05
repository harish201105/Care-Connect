# pages.py
import streamlit as st
from components.pages.dashboard import DashboardPage
from components.pages.health_profile import HealthProfilePage
from components.pages.doctor_profile import DoctorProfilePage
from components.pages.ai_health_assistant import AIHealthAssistantPage
from components.pages.health_surfers import HealthSurfersPage
from components.pages.physio_hub import PhysioHubPage
from components.pages.care_ring import CareRingPage

class Pages:
    def render(self):
        """Main rendering logic based on the current page"""
        if st.session_state.page == 'My Profile':
            self.profile_page()
        elif st.session_state.page == 'home':
            DashboardPage().render()
        elif st.session_state.page == 'ai_health_assistant':
            AIHealthAssistantPage().render()
        elif st.session_state.page == 'health_surfers':
            HealthSurfersPage().render()
        elif st.session_state.page == 'physio_hub':
            PhysioHubPage().render()
        elif st.session_state.page == 'care_ring':
            CareRingPage().render()
        elif st.session_state.page == 'health_profile':
            HealthProfilePage().render()
        elif st.session_state.page == 'doctor_profile':
            DoctorProfilePage().render()
        elif st.session_state.page == 'logout':
            st.subheader("Logout Page")

    def profile_page(self):
        st.write("Name: John Doe")
        st.write("Patient ID: ABC123")
        if st.button("My Health", key='my_health_button'):
            st.session_state.page = 'health_profile'
        if st.button("My Doctor", key='my_doctor_button'):
            st.session_state.page = 'doctor_profile'
        if st.button("Back to Home", key='back_to_home_button'):
            st.session_state.page = 'home'
