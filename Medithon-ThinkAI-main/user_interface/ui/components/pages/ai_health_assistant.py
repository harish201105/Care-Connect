from components.pages.base_page import Page

import streamlit as st
from llm_engine.personal_assistant import PersonalAssistant

class AIHealthAssistantPage(Page):
    def __init__(self):
        # Initialize the personal assistant
        self.assistant = PersonalAssistant()

    def render(self):
        """Render the UI for the chat page."""
        st.title('Personal Assistant')

        # Create an input field for user query
        user_prompt = st.text_input("Enter your query from the discharge summary")

        # Button to trigger vector embedding creation, only if embeddings aren't already created
        if 'vectors' not in st.session_state:
            if st.button("Create Document Embeddings"):
                self.assistant.create_vector_embedding()  # Create embeddings
                st.success("Vector Database is ready")
        else:
            st.success("Vector Database is already loaded")  # Embeddings already created

        # If the user has entered a query, process the LLM
        if user_prompt:
            st.write("Processing your query...")

            try:
                result = self.assistant.get_response(user_prompt)

                # Display response time and answer
                st.write(f"Response time: {result['response_time']} seconds")
                st.write(f"Answer: {result['answer']}")

            except Exception as e:
                st.error(f"Error: {str(e)}")

        # Go Back button to navigate to the dashboard
        if st.button("Go Back"):
            st.session_state['current_page'] = 'home'  # Set session state to go back to the dashboard
            
# if __name__ == '__main__':
#     ChatPage().render()
