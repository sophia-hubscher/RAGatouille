#!/usr/bin/env python3

import flask
import os
from flask_cors import CORS
from RAG_beta import RAGSystem

app = flask.Flask(__name__)
CORS(app)

rag_system = RAGSystem(api_key=os.getenv("OPENAI_API_KEY"))
rag_system.store_embeddings("https://en.wikipedia.org/wiki/ISO_New_England")

@app.route("/")
def home():
    return "System initialized!"

@app.route("/retrieve", methods=["POST"])
def retrieve():
    print("Retrieving information...")
    data = flask.request.json
    user_query = data.get("user_query", "")   
    print(user_query)
    if not user_query:
        return flask.jsonify({"error": "No query provided"}), 400
    
    try:
        retrieved_info = rag_system.get_response(user_query)
        return flask.jsonify({"retrievedInfo": retrieved_info})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
