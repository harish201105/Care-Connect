# healthsurfers_page.py
import streamlit as st

class HealthSurfersPage():
    """Class for rendering the Health Surfers page."""

    def __init__(self):
        super().__init__()
        self.set_page_title("Health Surfers Portal")

    def render(self):
        """Renders the Health Surfers page content."""
        self.display_title()
        st.write("Welcome to the Health Surfers Page!")
        st.write("Explore health tips, track fitness, and browse personalized content.")

        # Add more custom content for the Health Surfers page here
        st.text_area("Share your health journey:")
        st.button("Submit Story")

        self.common_footer()
