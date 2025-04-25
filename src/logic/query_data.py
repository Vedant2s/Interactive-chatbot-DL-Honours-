import argparse
import os
import shap
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from get_embedding_function import get_embedding_function
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

CHROMA_PATH = "chroma"
PROMPT_TEMPLATE_FILE = "prompt_template.txt"

if os.path.exists(PROMPT_TEMPLATE_FILE):
    with open(PROMPT_TEMPLATE_FILE, "r") as f:
        PROMPT_TEMPLATE = f.read()
else:
    PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context in very short: {question}
"""

class ResponseModel(BaseModel):
    """Model for the structured response."""
    answer: str = Field(description="The answer to the question based on the context.")
    sources: list = Field(description="List of sources used to generate the answer.")
    top_contributing_words: list = Field(description="List of top contributing words.")

def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)
    print(json.dumps(structured_response))

from rank_bm25 import BM25Okapi
from typing import List

def query_rag(query_text: str):
    # Prepare the database and embedding function
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    
    # Get all documents from ChromaDB for BM25
    all_docs = db.get()['documents']  # List of all document texts
    tokenized_docs = [doc.split() for doc in all_docs]  # BM25 requires tokenized docs
    
    # Initialize BM25 and calculate scores
    bm25 = BM25Okapi(tokenized_docs)
    tokenized_query = query_text.split()
    bm25_scores = bm25.get_scores(tokenized_query)
    
    # Get semantic search results with scores from ChromaDB
    semantic_results = db.similarity_search_with_score(query_text, k=len(all_docs))
    
    # Normalize scores and combine (BM25 + Cosine Similarity)
    combined_results = []
    for i, (doc, cos_score) in enumerate(semantic_results):
        # Normalize scores to 0-1 range
        norm_cos = (cos_score + 1) / 2  # Cosine similarity ranges from -1 to 1
        norm_bm25 = (bm25_scores[i] - min(bm25_scores)) / (max(bm25_scores) - min(bm25_scores) + 1e-9)
        
        # Weighted combination (adjust weights as needed)
        combined_score = 0.9 * norm_cos + 0.1 * norm_bm25
        combined_results.append((doc, combined_score))
    
    # Sort by combined score and take top 2
    combined_results.sort(key=lambda x: x[1], reverse=True)
    top_results = combined_results[:5]  # Top 5 results
    
    # Format the context for the prompt
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in top_results])
    retrieved_contexts = [doc.page_content for doc, _score in top_results]
    
    # Generate prompt and get response
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    structured_response = get_structured_deepseek_response(prompt, top_results, context_text)
    
    # Format output
    formatted_response = f"{structured_response.answer}\n\nSources: {structured_response.sources}"
    print(formatted_response)
    print("Top Contributing Words:", structured_response.top_contributing_words)
    
    return structured_response.answer, retrieved_contexts


def get_structured_deepseek_response(prompt: str, results, context_text: str):
    device = torch.device("cpu")
    llm_model = ChatOllama(model="deepseek-r1:1.5b", temperature=0.1, device=device)
    structured_llm = llm_model.with_structured_output(ResponseModel, method="json_schema")

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    structured_response = structured_llm.invoke(prompt)
    structured_response.sources = sources

    # Explainability: Add top contributing words
    structured_response.top_contributing_words = compute_top_contributing_words(context_text)

    return structured_response

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def compute_top_contributing_words(context_text: str, top_k: int = 5):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform([context_text])
    feature_names = vectorizer.get_feature_names_out()
    scores = X.toarray()[0]

    top_indices = np.argsort(scores)[-top_k:][::-1]
    top_words = [feature_names[i] for i in top_indices]

    return top_words


if __name__ == "__main__":
    main()

