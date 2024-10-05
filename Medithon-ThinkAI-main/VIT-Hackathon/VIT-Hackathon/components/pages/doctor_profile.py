# doctor_profile.py
import streamlit as st
import pandas as pd
from components.pages.base_page import Page

class DoctorProfilePage(Page):
    def render(self):
        st.subheader("Doctor's Profile")

        # Creating a DataFrame for doctor profile details
        doctor_data = {
            'Field': ['Doctor Name', 'Contact No', 'Last Checkup'],
            'Details': ['Dr. Sushan Chao', '9176274608', 'Sept 05, 2024']
        }
        doctor_df = pd.DataFrame(doctor_data)
        
        # Display the DataFrame as a table
        st.table(doctor_df)
        
        # Back to Profile button
        if st.button("Back to Profile", key='back_to_profile_button'):
            st.session_state.page = 'My Profile'
