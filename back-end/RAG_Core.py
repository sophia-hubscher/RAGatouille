#!/usr/bin/env python3
import os
import openai
import logging
import traceback
import uuid
import ast

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

class AzureCognitiveSearchRetriever:
    """
    A retriever to query Azure Cognitive Search vector index.
    """
    def __init__(self, search_client, embedding_fn, k=5):
        self.search_client = search_client
        self.embedding_fn = embedding_fn
        self.k = k

    def get_relevant_documents(self, query):
        # Generate the query embedding

        # Perform vector search
        results = self.search_client.search(
            search_text=query,  # Empty for pure vector search
            top=self.k,
            include_total_count=True
        )

        # Parse results into a list of documents
        docs = []
        for result in results:
            doc = {
                "page_content": result["chunk"],  # Use the 'chunk' field for content
                "metadata": {
                    "chunk_id": result.get("chunk_id"),
                    "parent_id": result.get("parent_id"),
                    "title": result.get("title")
                }
            }
            docs.append(doc)

        return docs

class PDFRAGSystem:
    def __init__(self, api_key, search_endpoint, search_api_key, index_name, model_name="gpt-4o-mini"):
        self.api_key = api_key
        self.model_name = model_name

        # Initialize embeddings and LLM
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
        self.llm = ChatOpenAI(
            model_name=self.model_name,
            openai_api_key=self.api_key,
            temperature=0
        )

        # Azure Cognitive Search Clients
        self.search_endpoint = search_endpoint
        self.search_api_key = search_api_key
        self.index_name = index_name

        self.search_client = SearchClient(
            endpoint=self.search_endpoint,
            index_name=self.index_name,
            credential=AzureKeyCredential(self.search_api_key)
        )

        # Initialize the retriever
        self.retriever = AzureCognitiveSearchRetriever(
            search_client=self.search_client,
            embedding_fn=self.embeddings.embed_documents,
            k=5
        )

    def get_response(self, user_query):
        """Get response for a user query using the vectorized data from Azure Cognitive Search."""
        try:
            # Retrieve relevant documents
            relevant_docs = self.retriever.get_relevant_documents(user_query)
            print(f"Found {len(relevant_docs)} relevant documents.")
            print(relevant_docs)

            # Build the context from the retrieved documents
            context = "\n\n".join([doc["page_content"] for doc in relevant_docs])

            # Construct the prompt
            prompt = f"""You are a helpful AI assistant. Use the following context to answer the question.
            If you cannot find the answer in the context, say so - don't make up information.

            Context:
            {context}

            Question:
            {user_query}

            Answer:
            """

            # Call the LLM
            response = self.llm(prompt)
            answer = response.content.strip()

            # Extract source filenames (if available in metadata)
            sources = []
            for doc in relevant_docs:
                meta = doc["metadata"]
                if isinstance(meta, str):
                    meta = ast.literal_eval(meta)
                sources.append(doc["page_content"])
            return {
                "answer": answer,
                "sources": list(set(sources))
            }

        except Exception as e:
            print("Exception in get_response:", traceback.format_exc())
            return {
                "answer": "Sorry, there was an error processing your request.",
                "sources": [],
                "error": str(e)
            }