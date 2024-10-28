# -*- coding: utf-8 -*-
"""pdf_dowloader.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1I2yXHIhUc_adZplhrnvqOAn0EZaLPNPh
"""

!pip install chromadb
!pip install langchain
!pip install PyPDF2
!pip install tiktoken
!pip install openai
!pip install langchain_community
!pip install langchain_openai
!pip install flask
!pip install flask_cors

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

def download_pdf(url, output_dir):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '').lower()
            if 'application/pdf' in content_type:
                filename = os.path.join(output_dir, url.split('/')[-1])
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                print(f"Downloaded: {filename}")
            else:
                print(f"Not a PDF: {url}")
        else:
            print(f"Failed to download: {url}")
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

def get_pdf_links(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        pdf_links = []
        for link in links:
            href = link.get('href')
            if href and href.lower().endswith('.pdf'):
                full_url = urljoin(url, href)
                pdf_links.append(full_url)
        return pdf_links
    except Exception as e:
        print(f"Error fetching links from {url}: {str(e)}")
        return []

def main():
    urls = [
        "https://www.iso-ne.com/participate/rules-procedures/tariff",
        "https://www.iso-ne.com/participate/rules-procedures/manuals",
        "https://www.iso-ne.com/participate/rules-procedures/operating-procedures",
        "https://www.iso-ne.com/participate/rules-procedures/system-operating-procedures",
        "https://www.iso-ne.com/participate/rules-procedures/master-lcc-procedures",
        "https://www.iso-ne.com/participate/rules-procedures/generator-nongenerator-var-capability",
        "https://www.iso-ne.com/participate/rules-procedures/planning-procedures",
        "https://www.nerc.com/Pages/default.aspx"
    ]

    base_output_dir = "downloaded_pdfs"

    for url in urls:
        print(f"Processing: {url}")
        domain = urlparse(url).netloc
        output_dir = os.path.join(base_output_dir, domain)
        os.makedirs(output_dir, exist_ok=True)

        pdf_links = get_pdf_links(url)
        for pdf_url in pdf_links:
            download_pdf(pdf_url, output_dir)
            time.sleep(3)

        print(f"Finished processing: {url}")
        print("---")

if __name__ == "__main__":
    main()

from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import flask
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)

class PDFRAGSystem:
    def __init__(self, api_key, model_name="gpt-4"):
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
        try:
            # Create text splitter for chunking
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
            )

            # Load all PDFs from directory and subdirectories
            loader = DirectoryLoader(
                pdf_directory,
                glob="**/*.pdf",  # Match PDFs in all subdirectories
                loader_cls=PyPDFLoader
            )
            documents = loader.load()

            # Split documents into chunks
            split_documents = text_splitter.split_documents(documents)

            # Create vector store
            self.vector_store = Chroma.from_documents(
                documents=split_documents,
                embedding=self.embeddings,
                persist_directory="./chroma_db"  # Persist embeddings to disk
            )

            # Set up retriever
            self.retriever = self.vector_store.as_retriever(
                search_kwargs={"k": 5}  # Return top 5 most relevant chunks
            )

            return f"Successfully processed {len(documents)} PDFs"

        except Exception as e:
            return f"Error processing PDFs: {str(e)}"

    def get_response(self, user_query):
        """Get response for user query using RAG."""
        if not self.retriever:
            raise ValueError("PDFs must be processed before querying.")

        # Create the retrieval chain with custom prompt
        template = """You are an AI assistant helping with questions about ISO New England and related energy policies.
        Use the following context to answer the question. If you don't know or can't find the answer in the context,
        say so - don't make up information.

        Context: {context}

        Question: {question}
        """

        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.retriever,
            chain_type="stuff",
            return_source_documents=True,  # Include source documents in response
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
            if hasattr(doc.metadata, 'source'):
                sources.append(doc.metadata['source'])

        return {
            "answer": answer,
            "sources": list(set(sources))  # Remove duplicate sources
        }

# Initialize the RAG system
rag_system = PDFRAGSystem(api_key="API- Key")

@app.route("/")
def home():
    return "PDF RAG System initialized!"

@app.route("/process_pdfs", methods=["POST"])
def process_pdfs():
    """Endpoint to process PDFs and create embeddings."""
    try:
        result = rag_system.load_pdfs()
        return flask.jsonify({"message": result})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500

@app.route("/retrieve", methods=["POST"])
def retrieve():
    """Endpoint to query the RAG system."""
    print("Retrieving information...")
    data = flask.request.json
    user_query = data.get("user_query", "")
    print(f"Query received: {user_query}")

    if not user_query:
        return flask.jsonify({"error": "No query provided"}), 400

    try:
        response = rag_system.get_response(user_query)
        return flask.jsonify({
            "answer": response["answer"],
            "sources": response["sources"]
        })
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)