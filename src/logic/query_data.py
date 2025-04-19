import argparse
import os
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from get_embedding_function import get_embedding_function
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser

CHROMA_PATH = "chroma"
PROMPT_TEMPLATE_FILE = "prompt_template.txt"

# Load the prompt template from file if it exists,
# otherwise, use the default prompt template.
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

def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)

def query_rag(query_text: str):
    # Prepare the database with the updated embedding function.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB for similar documents.
    results = db.similarity_search_with_score(query_text, k=2)

    # Format the context for the prompt.
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    retrieved_contexts = [doc.page_content for doc, _score in results]  # List of contexts
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Initialize the model and get a structured response.
    structured_response = get_structured_deepseek_response(prompt, results)

    # Format and print the response.
    formatted_response = f"{structured_response.answer}\n\nSources: {structured_response.sources}"
    print(formatted_response)

    # Return both the predicted answer and the list of retrieved contexts
    return structured_response.answer, retrieved_contexts


# def get_structured_deepseek_response(prompt: str, results):
#     llm_model = ChatOllama(model="deepseek-r1:1.5b", temperature=0)
#     structured_llm = llm_model.with_structured_output(ResponseModel, method="json_schema")

#     # Extract sources from results.
#     sources = [doc.metadata.get("id", None) for doc, _score in results]

#     # Invoke the LLM with the prompt and structured output.
#     structured_response = structured_llm.invoke(prompt)
#     structured_response.sources = sources  # Add sources to the structured response.

#     return structured_response
import os
import torch
from langchain_ollama import ChatOllama

def get_structured_deepseek_response(prompt: str, results):
    import tensorflow as tf
    print("GPU Available: ", tf.config.list_physical_devices('GPU'))

    # Set the device to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Initialize the model with GPU support if available
    llm_model = ChatOllama(model="deepseek-r1:1.5b", temperature=0, device=device)
    structured_llm = llm_model.with_structured_output(ResponseModel, method="json_schema")

    # Extract sources from results.
    sources = [doc.metadata.get("id", None) for doc, _score in results]

    # Invoke the LLM with the prompt and structured output.
    structured_response = structured_llm.invoke(prompt)
    structured_response.sources = sources  # Add sources to the structured response.

    return structured_response

if __name__ == "__main__":
    main()
