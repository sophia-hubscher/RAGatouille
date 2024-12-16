# RAGatouille

A RAG (Retrieval-Augmented Generation) application with React frontend and Python backend, featuring document retrieval and an evaluation dashboard.

## Prerequisites

- Node.js (v14 or higher)
- Python (v3.8 or higher)
- Azure account with:
  - Azure Cognitive Search service
  - Azure Blob Storage
  - OpenAI API access

## Backend Setup

1. Navigate to the backend directory:
```bash
cd back-end
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install azure-storage-blob azure-search-documents langchain-openai openai
```

4. Configure environment variables:
```bash
export AZURE_STORAGE_CONNECTION_STRING="your_storage_connection_string"
export OPENAI_API_KEY="your_openai_api_key"
export AZURE_SEARCH_ENDPOINT="your_search_endpoint"
export AZURE_SEARCH_KEY="your_search_api_key"
```

5. Document upload setup:
- Place your PDF/DOCX files in `back-end/downloaded_pdfs`
- Run the uploader:
```bash
python document_uploader.py
```

6. Start the RAG system:
```bash
python App.py
```

## Frontend Setup

1. Main application setup:
```bash
cd front-end
npm install
npm start
```
Access the main application at `http://localhost:3000`

2. Evaluation dashboard setup:
```bash
cd eval-front-end
npm install
npm start
```
Access the evaluation dashboard at `http://localhost:3001`

## Project Structure

```
RAGatouille/
├── back-end/
│   ├── downloaded_pdfs/     # Source documents directory
│   ├── RAG_Core.py         # RAG implementation
│   └── document_uploader.py # Azure Blob Storage uploader
├── front-end/              # Main React application
│   ├── src/
│   └── public/
└── eval-front-end/         # Evaluation dashboard
    ├── src/
    └── public/
```

## Features

- Document processing and storage in Azure Blob Storage
- Vector search using Azure Cognitive Search
- RAG-powered question answering
- Interactive React frontend
- Evaluation dashboard with metrics visualization
- Support for PDF and DOCX documents

## Technical Details

### Backend
- Uses OpenAI's embeddings and language models
- Azure Cognitive Search for vector storage and retrieval
- Implements RAG pattern for accurate information retrieval

### Frontend
- React-based user interface
- Chart.js for metrics visualization
- Responsive design with dark theme
- Real-time data updates

## Important Notes

- Ensure Azure services are properly configured before use
- Keep environment variables secure and never commit them
- Backend must be running for frontend functionality
- Monitor API usage to manage costs

## Troubleshooting

1. If documents fail to upload:
   - Check Azure connection string
   - Verify file permissions
   - Ensure supported file formats

2. If search isn't working:
   - Verify Azure Search endpoint and key
   - Check if documents are properly indexed
   - Monitor Azure Search service status

3. Frontend connection issues:
   - Confirm backend is running
   - Check for CORS configuration
   - Verify API endpoint configuration