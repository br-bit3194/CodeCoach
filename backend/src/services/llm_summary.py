
# Uses GPT-4 to summarize code content
from openai import OpenAI

from ..core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def summarize_code(file_content: str, file_path: str):
    # Construct a smart prompt to summarize the file for documentation and diagram purposes
    prompt = f"""
You are an expert software engineer. Summarize the purpose of the following Python file and provide a one-liner for inclusion in a Mermaid.js tree diagram.

Filename: {file_path}
Code:
{file_content[:3000]}

Return:
1. Summary of the file's purpose.
2. A one-liner node label for the file, e.g., 'models/user.py: defines User ORM'.
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

def summarize_project(project_metadata: dict, file_summaries: list):
    """
    Generates a full application-level summary using metadata and all file summaries and overall.
    """
    prompt = f"""
You are an expert software architect. Given the following metadata and file summaries, generate a complete project overview.

Metadata:
{project_metadata}

Files:
{file_summaries[:3000]}  # truncate if needed

Return a summary that includes:
- Project purpose
- Main service or domain focus
- Architecture type (monolith, microservices)
- Frameworks and dependencies
- Database/infra mentions (from code if any)
- Observations about standards, structure, naming
- Anything worth improving
- One-liner architecture description
"""

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content
