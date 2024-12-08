#!/usr/bin/env python3
import os
from azure.storage.blob import BlobServiceClient

# Replace with your Azure Storage account connection string
CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "all-docs"  # Replace with your container name

def upload_files_to_blob(root_folder):
    try:
        # Create a BlobServiceClient object
        blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)

        # Ensure the container exists (create if it doesn't)
        if not container_client.exists():
            container_client.create_container()

        # Traverse the root folder and find .pdf and .docx files
        for root, _, files in os.walk(root_folder):
            for file in files:
                if file.endswith(('.pdf', '.docx')):
                    file_path = os.path.join(root, file)
                    blob_name = file  # Use only the file name as the blob name

                    # Upload the file to Azure Blob Storage
                    blob_client = container_client.get_blob_client(blob_name)
                    with open(file_path, "rb") as data:
                        blob_client.upload_blob(data, overwrite=True)
                    
                    print(f"Uploaded: {file_path} as {blob_name}")

    except Exception as ex:
        print(f"An error occurred: {ex}")


# Replace with the path to your root folder containing the files
ROOT_FOLDER = "/Users/shiven/Desktop/RAGatouille/back-end/downloaded_pdfs"

upload_files_to_blob(ROOT_FOLDER)