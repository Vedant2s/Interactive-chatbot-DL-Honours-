import os
import time
import re  # Import regex for stripping out <think>...</think>
from datasets import load_dataset
from populate_database import add_to_chroma
from query_data import query_rag
from langchain.schema.document import Document
from langchain_ollama import ChatOllama
from get_embedding_function import get_embedding_function


print("LANGSMITH_API_KEY:", os.environ.get("LANGSMITH_API_KEY"))
print("LANGSMITH_ENDPOINT:", os.environ.get("LANGSMITH_ENDPOINT"))
print("LANGSMITH_PROJECT:", os.environ.get("LANGSMITH_PROJECT"))


ds_qa = load_dataset("rag-datasets/rag-mini-wikipedia", "question-answer", split="test")
ds_corpus = load_dataset("rag-datasets/rag-mini-wikipedia", "text-corpus", split="passages")


llm_model = ChatOllama(model="deepseek-r1:1.5b", temperature=0)
local_embeddings = get_embedding_function()


documents = [
    Document(page_content=passage, metadata={"id": str(idx)})
    for idx, passage in enumerate(ds_corpus["passage"])
]
add_to_chroma(documents)  

total_questions = 10  
local_dataset = []
total_response_time = 0


from langsmith import Client, wrappers
from pydantic import BaseModel, Field

client = Client()

dataset_name = "Sample datasetR1"
description = "A sample dataset created from rag-mini-wikipedia QA"

try:
    dataset = client.create_dataset(
        dataset_name=dataset_name,
        description=description
    )
except Exception as e:
    if "Dataset with this name already exists" in str(e):
        datasets = client.list_datasets()
        dataset = next(ds for ds in datasets if ds.name == dataset_name)
        print(f"Dataset '{dataset_name}' already exists. Using the existing dataset.")
    else:
        raise e

examples = []
for q, a in zip(ds_qa["question"][:total_questions], ds_qa["answer"][:total_questions]):
    examples.append({
        "inputs": {"question": q},
        "outputs": {"answer": a}
    })

client.create_examples(dataset_id=dataset.id, examples=examples)

def target(inputs: dict) -> dict:
    question = inputs["question"]
    predicted_answer, _ = query_rag(question)
    return {"response": predicted_answer}

instructions = (
    "Evaluate Student Answer against Ground Truth for conceptual similarity and classify true or false:\n"
    "- False: No conceptual match or similarity\n"
    "- True: Most or full conceptual match and similarity\n"
    "Key criteria: The core concept should match, not necessarily the exact wording."
)

class Grade(BaseModel):
    score: bool = Field(
        description="Boolean indicating whether the response is accurate relative to the reference answer"
    )

def accuracy(outputs: dict, reference_outputs: dict) -> bool:
    prompt = (
        f"{instructions}\n\n"
        f"Ground Truth answer: {reference_outputs['answer']}\n"
        f"Student's Answer: {outputs['response']}\n"
        "Respond with True or False."
    )
    response = llm_model.invoke(prompt)
    if hasattr(response, "content"):
        answer_str = response.content
    else:
        answer_str = str(response)
    answer_str = re.sub(r"<think>.*?</think>", "", answer_str, flags=re.DOTALL)
    answer_str = answer_str.strip().lower()
    return answer_str == "true"

experiment_results = client.evaluate(
    target,
    data=dataset.id,  
    evaluators=[accuracy],
    experiment_prefix="first-eval-in-langsmithR1",
    max_concurrency=2,
)

print("LangSmith Experiment Results:")
print(experiment_results)
