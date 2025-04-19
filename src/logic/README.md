# Project Name : AI-Powered Contextual Query Answering with Retrieval-Augmented Generation

This project provides a framework for managing and querying a ChromaDB database with embeddings, powered by the Gemini AI Studio API. Follow the steps below to install required packages, prepare your data, and query the database.

## Requirements

To install the necessary packages, open your terminal and run:

```bash
pip install -r requirements.txt
```
### We need to install Visual Studio Build Tools for successfully installing ChromaDB 
## Add Your Source Context Files
In the data folder of the project package, you can add your own source context documents (e.g., PDFs) that you want to use as reference material for the chat application. Once added, make sure to run the populate_database.py script to store the documents in ChromaDB as embeddings.

Run the following command:
```bash
python populate_database.py
```

## Set Your API Key
This project uses Gemini AI Studio for generating text embeddings. You need to set your API key in two files: query_data.py and get_embedding_function.py.

Open `query_data.py` and `get_embedding_function.py`
Locate the line for setting the API key and replace it with your Gemini AI Studio API key

```python
API_KEY = "your_gemini_api_key_here"
```
## Run a Query
To query the database, use the following command format in the terminal:

```python
python query_data.py "Your query text here"
```
Replace "Your query text here" with the specific question or query you have for the database.

## Folder Structure

* requirements.txt - List of packages required for the project.
* data/ - Folder to store source context files (e.g., PDFs).
* populate_database.py - Script to populate ChromaDB with embeddings for each document in data.
* query_data.py - Script to submit queries and retrieve responses.
* get_embedding_function.py - Contains functions for generating embeddings using Gemini AI Studio.
