#!/usr/bin/env python3


from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI  # Updated import
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

# Load documents
loader = WebBaseLoader("https://en.wikipedia.org/wiki/Retrieval-augmented_generation")
documents = loader.load()

# Create embeddings
embeddings = OpenAIEmbeddings(openai_api_key='Add your key here')

# Create a vector store
vector_store = Chroma.from_documents(documents, embedding=embeddings)

# Set up the retriever
retriever = vector_store.as_retriever()

# Initialize the language model
llm = ChatOpenAI(model_name="gpt-4o-mini")

# Create the retrieval chain without the prompt parameter
retrieval_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# Get user input and retrieve information
user_query = input("Please enter your query: ")
retrieved_info = retrieval_chain.invoke({"query": user_query})
response = f"User Query: {user_query}\nRetrieved Information: {retrieved_info}"
print(response)
