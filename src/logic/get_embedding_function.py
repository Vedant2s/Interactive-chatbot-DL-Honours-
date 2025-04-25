# import google.generativeai as genai

# API_KEY="AIzaSyA4Y5rFR80mqEDYxc_W0abSpviGXidx2Ag"
# genai.configure(api_key=API_KEY)

# class GoogleEmbeddingWrapper:
#     def embed_documents(self, texts):
#         # Generate embeddings for a list of texts
#         embeddings = []
#         for text in texts:
#             embedding = genai.embed_content(
#                 model="models/text-embedding-004",
#                 content=text,
#                 task_type="retrieval_document",
#                 title="Embedding of single string"
#             )
#             embeddings.append(embedding['embedding'])  # Ensure this is the correct field for the embedding vector
#         return embeddings

#     def embed_query(self, text):
#         # Generate an embedding for a single query text
#         embedding = genai.embed_content(
#             model="models/text-embedding-004",
#             content=text,
#             task_type="retrieval_document",
#             title="Embedding of single string"
#         )
#         return embedding['embedding']  # Ensure this is the correct field for the embedding vector

# def get_embedding_function():
#     return GoogleEmbeddingWrapper()






import requests

class OllamaEmbeddingWrapper:
    def __init__(self, base_url="http://localhost:11434/api/embeddings"):
        self.base_url = base_url

    def embed_documents(self, texts):
        embeddings = []
        for text in texts:
            embedding = self._get_embedding(text)
            embeddings.append(embedding)
        return embeddings

    def embed_query(self, text):
        return self._get_embedding(text)

    def _get_embedding(self, text):
        response = requests.post(
            self.base_url,
            json={
                "model": "nomic-embed-text",
                "prompt": text
            }
        )
        response.raise_for_status() 
        return response.json().get('embedding')  

def get_embedding_function():
    return OllamaEmbeddingWrapper()
