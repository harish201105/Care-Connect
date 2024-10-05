# health_surfers.py
import streamlit as st
from components.pages.base_page import Page

class HealthSurfersPage(Page):
    def render(self):
        st.subheader("Health Surfers - VR Game")
        st.write("Engage in a fun and interactive VR game designed to improve your health!")
