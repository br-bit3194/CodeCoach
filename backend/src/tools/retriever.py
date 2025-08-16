"""Module providing a langchain tool for code retriever."""
import os
from langchain_core.tools import tool
import faiss, json
import numpy as np

from ..core.config import settings
from ..services.embedding import get_embedding

def load_faiss_index(index_dir_path):
    """Load FAISS index and docs.pkl correctly."""
    import pickle
    index = faiss.read_index(os.path.join(index_dir_path, "index.faiss"))
    with open(os.path.join(index_dir_path, "index.pkl"), "rb") as f:
        docs = pickle.load(f)  # use pickle.load, NOT readlines
    return index, docs


@tool
def get_code_context(concised_question: str, top_k=settings.DOC_RETRIEVAL_TOP_K):
    """ This tool provides relevant code information for the given question"""
    index_dir_path = os.path.join(os.getcwd(), "faiss_index")
    index, docs = load_faiss_index(index_dir_path)
    question_embedding = get_embedding(concised_question)

    # Search top_k similar docs
    D, I = index.search(np.array([question_embedding]).astype('float32'), top_k)

    results = []
    for i in I[0]:
        if i < len(docs):
            results.append(json.dumps(docs[i]).strip())

    if not results:
        return "No relevant documents found."

    coding_files_info = "Following are the relevant coding files I found:\n\n"
    coding_files_info += "\n\n---\n\n".join(results)
    return coding_files_info