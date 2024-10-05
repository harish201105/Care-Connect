# health_profile.py
import streamlit as st
import pandas as pd
from components.pages.base_page import Page

class HealthProfilePage(Page):
    def render(self):
        st.subheader("Health Profile Page")
        
        # Creating a DataFrame for health profile details
        health_data = {
            'Field': ['Age', 'Gender', 'Previous Medical History', 'Recovery Period', 'Current Condition'],
            'Details': ['32', 'Male', 'Dengue', '4 weeks', 'Normal']
        }
        health_df = pd.DataFrame(health_data)
        
        # Display the DataFrame as a table
        st.table(health_df)
        
        # Back to Profile button
        if st.button("Back to Profile", key='back_to_profile_button'):
            st.session_state.page = 'My Profile'
