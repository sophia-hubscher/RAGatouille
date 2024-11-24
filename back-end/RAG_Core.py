#!/usr/bin/env python3
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

class PDFRAGSystem:
    def __init__(self, api_key, model_name="gpt-4o-mini"):
        self.api_key = api_key
        self.model_name = model_name
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
        self.llm = ChatOpenAI(
            model_name=self.model_name,
            openai_api_key=self.api_key,
            temperature=0
        )
        self.vector_store = None
        self.retriever = None

    def load_pdfs(self, pdf_directory="downloaded_pdfs"):
        """Load PDFs from the specified directory and its subdirectories."""
        persist_directory = "chroma_db"
        try:
            if os.path.exists(persist_directory):
                # Load existing vector store
                self.vector_store = Chroma(
                    persist_directory=persist_directory,
                    embedding_function=self.embeddings
                )
                self.retriever = self.vector_store.as_retriever(
                    search_kwargs={"k": 5}
                )
                return "Successfully loaded existing embeddings from disk."
            else:
                # Create text splitter for chunking
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len,
                )

                # Load all PDFs from directory and subdirectories
                loader = DirectoryLoader(
                    pdf_directory,
                    glob="**/*.pdf",
                    loader_cls=PyPDFLoader
                )
                print(f"Loading PDFs from {pdf_directory}...")
                try:
                    documents = loader.load()
                    print(f"Loaded {len(documents)} documents.")
                except Exception as e:
                    print(f"Error loading documents: {str(e)}")
                    return f"Error loading documents: {str(e)}"

                # Split documents into chunks
                split_documents = text_splitter.split_documents(documents)

                # Create vector store
                self.vector_store = Chroma.from_documents(
                    documents=split_documents,
                    embedding=self.embeddings,
                    persist_directory=persist_directory
                )

                # Set up retriever
                self.retriever = self.vector_store.as_retriever(
                    search_kwargs={"k": 10}
                )

                return f"Successfully processed {len(documents)} PDFs"

        except Exception as e:
            return f"Error processing PDFs: {str(e)}"

    def get_response(self, user_query):
        """Get response for user query using RAG."""
        if not self.retriever:
            raise ValueError("PDFs must be processed before querying.")

        try:
            # Create the retrieval chain with custom prompt
            template = """You are an AI chatbot helping with questions about ISO New England and related energy policies.
            Use the following context to answer the question. If you don't know or can't find the answer in the context,
            say so - don't make up information.

            Context: {context}

            Question: {question}
            """

            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                retriever=self.retriever,
                chain_type="stuff",
                return_source_documents=True,
                chain_type_kwargs={
                    "prompt": PromptTemplate(
                        template=template,
                        input_variables=["context", "question"]
                    ),
                }
            )

            # Get response
            response = qa_chain({"query": user_query})

            # Format response with sources
            answer = response['result']
            sources = []
            for doc in response['source_documents']:
                if 'source' in doc.metadata:
                    sources.append(doc.metadata['source'])
            print(f"Answer: {answer}")
            return {
                "answer": answer,
                "sources": list(set(sources))
            }
        except Exception as e:
            # Print the exception to the console for debugging
            import traceback
            print("Exception in get_response:", traceback.format_exc())
            print(sources)
            return {
                "answer": "Sorry, there was an error processing your request.",
                "sources": [],
                "error": str(e)
            }