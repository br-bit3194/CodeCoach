import os
import ast
import uuid
from openai import OpenAI
import faiss
import pickle
import numpy as np
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

from ..core.config import settings
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
client = OpenAI(api_key=settings.OPENAI_API_KEY)

# ========== AST Chunker ==========
def extract_code_chunks(code: str, filename: str):
    chunks = []
    try:
        tree = ast.parse(code)
        lines = code.splitlines()
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                start = node.lineno - 1
                end = _get_end_line(node) - 1
                chunk = "\n".join(lines[start:end + 1])
                if chunk.strip():
                    chunks.append({
                        "id": str(uuid.uuid4()),
                        "filename": filename,
                        "name": getattr(node, 'name', None),
                        "type": type(node).__name__,
                        "docstring": ast.get_docstring(node),
                        "code": chunk
                    })
    except Exception as e:
        print(f"Failed to parse {filename}: {e}")
    return chunks

def _get_end_line(node):
    max_lineno = getattr(node, 'lineno', -1)
    for child in ast.iter_child_nodes(node):
        child_end = _get_end_line(child)
        if child_end > max_lineno:
            max_lineno = child_end
    return max_lineno

# ========== Repo Walker ==========
def chunk_repo(path):
    all_chunks = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        code = f.read()
                        chunks = extract_code_chunks(code, full_path)
                        all_chunks.extend(chunks)
                except Exception as e:
                    print(f"Failed to read {full_path}: {e}")
    return all_chunks

# ========== Embedding ==========
def get_embedding(text, model="text-embedding-3-small"):
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding  # ✅ CORRECT way

def embed_chunk(chunk):
    try:
        embedding = get_embedding(chunk["code"])
        return {
            "embedding": embedding,
            "metadata": chunk,
            "success": True
        }
    except Exception as e:
        return {
            "error": str(e),
            "metadata": chunk,
            "success": False
        }

# ========== Main Logic ==========
def build_faiss_index(chunks, save_path):
    embeddings = []
    metadata = []

    with ThreadPoolExecutor(max_workers=5) as executor:  # Tune worker count as needed
        futures = [executor.submit(embed_chunk, chunk) for chunk in chunks]

        for future in as_completed(futures):
            result = future.result()
            if result["success"]:
                embeddings.append(result["embedding"])
                metadata.append(result["metadata"])
                print(f"✅ Embedded: {result['metadata']['filename']} > {result['metadata']['name']}")
            else:
                print(f"❌ Failed to embed {result['metadata']['filename']} - {result['error']}")


    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype('float32'))

    os.makedirs(save_path, exist_ok=True)

    # Save FAISS index
    faiss.write_index(index, os.path.join(save_path, "index.faiss"))

    # Save metadata
    with open(os.path.join(save_path, "index.pkl"), "wb") as f:
        pickle.dump(metadata, f)

    print(f"🎉 FAISS index built with {len(embeddings)} chunks.")

# main function
def embed_documents(repo_path, save_path="faiss_index"):
    if os.path.exists(save_path):
        shutil.rmtree(save_path)
    chunks = chunk_repo(repo_path)
    build_faiss_index(chunks, save_path)