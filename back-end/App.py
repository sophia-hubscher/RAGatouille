#!/usr/bin/env python3

import flask
import os
from flask_cors import CORS
from RAG_Core import PDFRAGSystem

app = flask.Flask(__name__)
CORS(app)
rag_system = PDFRAGSystem(api_key=os.getenv("OPENAI_API_KEY"))


@app.route("/")
def home():
    return "System initialized!"

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
        if not rag_system.retriever:
            return flask.jsonify({"error": "PDFs must be processed before querying."}), 400

        response = rag_system.get_response(user_query)
        return flask.jsonify({
            "answer": response["answer"],
            "sources": response["sources"],
            "error": response.get("error", "")
        })
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    try:
        print("Initializing RAG system...")
        rag_system.load_pdfs()
        print("RAG system initialized")
    except Exception as e:
        print(f"Error initializing RAG system: {str(e)}")
    app.run(debug=True, port=5000)
