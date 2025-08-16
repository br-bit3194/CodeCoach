# Walks a directory and summarizes all Python files
import os
from .llm_summary import summarize_code
def summarize_codebase(base_dir: str):
    summaries = []
    for root, _, files in os.walk(base_dir):
        for f in files:
            if f.endswith(".py"):
                full_path = os.path.join(root, f)

                # Read file content
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()

                try:
                    # Generate summary using LLM
                    summary = summarize_code(content, os.path.relpath(full_path, base_dir))
                except Exception as e:
                    summary = f"Error summarizing file: {e}"

                # Store file info and summary
                summaries.append({
                    "file_path": os.path.relpath(full_path, base_dir),
                    "content": content,
                    "summary": summary
                })
    return summaries

def detect_project_metadata(base_dir: str):
    metadata = {}

    # Check for Python project
    if os.path.exists(os.path.join(base_dir, "requirements.txt")):
        metadata["language"] = "Python"
        metadata["frameworks"] = []
        with open(os.path.join(base_dir, "requirements.txt")) as f:
            metadata["dependencies"] = f.read().splitlines()
            if any("django" in d.lower() for d in metadata["dependencies"]):
                metadata["frameworks"].append("Django")
            if any("flask" in d.lower() for d in metadata["dependencies"]):
                metadata["frameworks"].append("Flask")

    # Check for Node.js project
    elif os.path.exists(os.path.join(base_dir, "package.json")):
        metadata["language"] = "JavaScript"
        import json
        with open(os.path.join(base_dir, "package.json")) as f:
            pkg = json.load(f)
            metadata["project_name"] = pkg.get("name")
            metadata["version"] = pkg.get("version")
            metadata["dependencies"] = pkg.get("dependencies", {})
            metadata["devDependencies"] = pkg.get("devDependencies", {})
            metadata["frameworks"] = []
            if "express" in metadata["dependencies"]:
                metadata["frameworks"].append("Express")

    # Future: Add Java, .NET, PHP...

    return metadata
