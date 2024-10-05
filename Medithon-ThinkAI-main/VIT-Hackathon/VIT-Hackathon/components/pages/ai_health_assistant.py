from components.pages.base_page import Page

import streamlit as st

import os
import time
import streamlit as st
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader

class PersonalAssistant:
    def __init__(self):
        # Load the API key
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        
        # Initialize the LLM
        self.llm = ChatGroq(groq_api_key=self.groq_api_key, model="Llama3-70b-8192")
        
        # Define the prompt template
        self.prompt = ChatPromptTemplate.from_template(
            """
            Your are very carring and kind medical assistant sarra
            <context>
            {context}
            <context>
            Question: {input}
            """
        )
        
        # Initialize variables for embeddings, loader, and vectors
        self.embeddings = None
        self.loader = None
        self.final_documents = None

    def create_vector_embedding(self):
        """Initialize embeddings, load documents, split text, and create vector embeddings."""
        if 'vectors' not in st.session_state:
            # Load embeddings model
            self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            self.loader = PyPDFDirectoryLoader("patient_data")  # Load documents from PDF directory
            docs = self.loader.load()  # Load all documents
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            self.final_documents = text_splitter.split_documents(docs)  # Split large documents into chunks

            # Create FAISS vector embeddings
            vectors = FAISS.from_documents(self.final_documents, self.embeddings)

            # Store vectors in session_state
            st.session_state['vectors'] = vectors
            st.success("Vector Database is ready and stored in session state")

        else:
            st.success("Vector Database is already loaded from session state")

    def get_response(self, user_prompt):
        """Get the response from the LLM based on the user query."""
        if 'vectors' not in st.session_state:
            raise ValueError("Vector database is not ready. Please create document embeddings first.")

        # Create the document chain
        document_chain = create_stuff_documents_chain(self.llm, self.prompt)

        # Retrieve vectors from session_state
        vectors = st.session_state['vectors']
        retriever = vectors.as_retriever()  # Create a retriever from the vector store

        # Create the retrieval chain
        retrieval_chain = create_retrieval_chain(retriever, document_chain)

        # Measure response time and get the response
        start = time.process_time()
        response = retrieval_chain.invoke({"input": user_prompt})
        end = time.process_time()

        # Return response time and answer
        return {
            "response_time": end - start,
            "answer": response.get('answer', 'No answer available'),
            # Uncomment the below lines to return source documents
            # "source_documents": response.get('context', [])
        }


class AIHealthAssistantPage(Page):
    def __init__(self):
        # Initialize the personal assistant
        # from components.pages.ai_health_assistant import PersonalAssistant
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
