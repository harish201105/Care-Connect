import streamlit as st

class Footer:
    def render(self):
        st.markdown("""
        <div style="position: fixed; bottom: 10px; width: 100%;">
            <hr style="border: 1px solid;">
            <span>Developed by Yenepova Medical Center, Mangalore, India</span>
            <button onclick="window.location.href='mailto:contact@yenepova.com';">Contact Us</button>
            <button onclick="window.location.href='https://www.yenepova.com/about';">About Us</button>
            <button onclick="window.location.href='https://www.yenepova.com/services';">Our Services</button>
        </div>
        """, unsafe_allow_html=True)
