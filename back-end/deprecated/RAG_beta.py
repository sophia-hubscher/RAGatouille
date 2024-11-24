#!/usr/bin/env python3
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

class RAGSystem:
    def __init__(self, api_key, model_name="gpt-4o-mini"):
        self.api_key = api_key
        self.model_name = model_name
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
        self.llm = ChatOpenAI(model_name=self.model_name, openai_api_key=self.api_key)
        self.vector_store = None
        self.retriever = None

    def store_embeddings(self, url):
        # Load documents
        loader = WebBaseLoader(url)
        documents = loader.load()
        
        # Create a vector store
        self.vector_store = Chroma.from_documents(documents, embedding=self.embeddings)
        
        # Set up the retriever
        self.retriever = self.vector_store.as_retriever()

# In RAG_beta.py, update the get_response method
    def get_response(self, user_query):
        if not self.retriever:
            raise ValueError("Embeddings must be stored before querying.")
        
        # Create the retrieval chain
        retrieval_chain = RetrievalQA.from_chain_type(llm=self.llm, retriever=self.retriever)
        
        # Retrieve information
        response_dict = retrieval_chain({"query": user_query})
        assistant_response = response_dict['result']
        return assistant_response  # This will be the assistant's response as a string

# Example usage
if __name__ == "__main__":
    api_key = ''
    rag_system = RAGSystem(api_key=api_key)
    
    # Store embeddings from a URL
    rag_system.store_embeddings("https://en.wikipedia.org/wiki/Retrieval-augmented_generation")
    
    # Get user input and retrieve information
    user_query = input("Please enter your query: ")
    response = rag_system.get_response(user_query)
    print(response)
