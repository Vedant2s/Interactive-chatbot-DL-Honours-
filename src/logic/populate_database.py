import argparse
import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from get_embedding_function import get_embedding_function
from langchain_chroma import Chroma

CHROMA_PATH = "chroma"
DATA_PATH = "data"

def main():
    try:
        # Check if the database should be cleared (using the --reset flag).
        parser = argparse.ArgumentParser()
        parser.add_argument("--reset", action="store_true", help="Reset the database.")
        args = parser.parse_args()
        if args.reset:
            print("Clearing Database")
            clear_database()

        # Create (or update) the data store.
        documents = load_documents()
        chunks = split_documents(documents)
        add_to_chroma(chunks)
    except Exception as e:
        print(f"An error occurred: {e}")

def load_documents():
    try:
        document_loader = PyPDFDirectoryLoader(DATA_PATH)
        return document_loader.load()
    except Exception as e:
        print(f"Error loading documents: {e}")
        return []

def split_documents(documents: list[Document]):
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=80,
            length_function=len,
            is_separator_regex=False,
        )
        return text_splitter.split_documents(documents)
    except Exception as e:
        print(f"Error splitting documents: {e}")
        return []

def add_to_chroma(chunks: list[Document]):
    try:
        # Initialize the Chroma database with the embedding wrapper
        db = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=get_embedding_function()  # This now returns an embedding wrapper with the required methods
        )

        # Calculate Page IDs
        chunks_with_ids = calculate_chunk_ids(chunks)

        # Add only new documents
        existing_items = db.get(include=[])
        existing_ids = set(existing_items["ids"])
        print(f"Number of existing documents in DB: {len(existing_ids)}")

        new_chunks = [chunk for chunk in chunks_with_ids if chunk.metadata["id"] not in existing_ids]

        if new_chunks:
            print(f"Adding new documents: {len(new_chunks)}")
            new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
            db.add_documents(new_chunks, ids=new_chunk_ids)  # Embeddings handled by GoogleEmbeddingWrapper
            # db.persist()
        else:
            print("No new documents to add")
    except Exception as e:
        print(f"Error adding to Chroma: {e}")

def calculate_chunk_ids(chunks):
    try:
        # This will create IDs like "data/monopoly.pdf:6:2"
        # Page Source : Page Number : Chunk Index
        last_page_id = None
        current_chunk_index = 0

        for chunk in chunks:
            source = chunk.metadata.get("source")
            page = chunk.metadata.get("page")
            current_page_id = f"{source}:{page}"

            # If the page ID is the same as the last one, increment the index.
            if current_page_id == last_page_id:
                current_chunk_index += 1
            else:
                current_chunk_index = 0

            # Calculate the chunk ID.
            chunk_id = f"{current_page_id}:{current_chunk_index}"
            last_page_id = current_page_id

            # Add it to the page meta-data.
            chunk.metadata["id"] = chunk_id

        return chunks
    except Exception as e:
        print(f"Error calculating chunk IDs: {e}")
        return []

def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

if __name__ == "__main__":
    main()


