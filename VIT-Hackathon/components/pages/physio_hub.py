# physio_hub.py
import streamlit as st
from components.pages.base_page import Page

class PhysioHubPage(Page):
    def render(self):
        st.subheader("Physio Hub - Workout Companion")
        st.write("Your personal workout companion to keep you fit and motivated.")
