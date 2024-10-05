# physio_hub.py
from components.pages.base_page import Page

import streamlit as st
import cv2
import mediapipe as mp
import numpy as np

class PhysioHubPage(Page):
    """Class for rendering the Physio page."""

    def __init__(self):
        super().__init__()
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils
        self.cap = None  # Initialize cap as None for camera control

    def set_page_title(self, title):
        """Set the title of the page."""
        st.set_page_config(page_title=title)

    def display_title(self):
        """Display the title of the page."""
        st.title("Physio Connect")

    def render(self):
        """Renders the Physio page content."""
        self.display_title()
        st.write("Welcome to the Physio Page!")
        st.write("Here you can manage your physiotherapy sessions, track progress, and more.")

        # Add buttons for camera control
        if 'camera_started' not in st.session_state:
            st.session_state.camera_started = False

        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Start Camera"):
                st.session_state.camera_started = True
        
        with col2:
            if st.button("Stop Camera"):
                st.session_state.camera_started = False

        with col3:
            if st.button("Back to Dashboard"):
                # Stop the camera and processing before navigating back
                self.stop_camera()
                st.session_state.page = "home"

        # Display camera feed if started
        if st.session_state.camera_started:
            self.run_camera()

        self.common_footer()

    def common_footer(self):
        st.write("Thank you for using Physio Connect!")

    def stop_camera(self):
        """Stop the camera and release resources."""
        if self.cap:
            st.session_state.camera_started = False
            self.cap.release()  # Release the camera
            cv2.destroyAllWindows()  # Close any OpenCV windows

    def run_camera(self):
        """Opens the camera and detects body keypoints using Mediapipe."""
        self.cap = cv2.VideoCapture(0)
        frame_window = st.image([])  # Initialize an empty frame window

        while st.session_state.camera_started:
            success, frame = self.cap.read()

            if not success:
                st.error("Unable to access the camera.")
                break

            # Convert frame to RGB as Mediapipe expects RGB input
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Perform pose detection
            results = self.pose.process(image_rgb)

            # Draw pose landmarks on the frame
            if results.pose_landmarks:
                self.mp_drawing.draw_landmarks(
                    image_rgb,
                    results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS
                )

            # Convert image back to BGR for OpenCV display
            image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

            # Update the Streamlit image placeholder with the new frame
            frame_window.image(image_bgr, channels="BGR")

            # Exit loop if Stop button or Back button is pressed
            if not st.session_state.camera_started:
                break

        # Ensure the camera is released and OpenCV windows are closed
        self.stop_camera()

