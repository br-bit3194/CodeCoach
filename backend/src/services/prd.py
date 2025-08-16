from pathlib import Path
from openai import OpenAI 
from dotenv import load_dotenv 
from tqdm import tqdm

from ..core.config import settings
load_dotenv() 

client = OpenAI(api_key=settings.OPENAI_API_KEY)
# allowed_folders = "/home/pushapanjalik/hackathon/ecommerce-microservices-dockerized_setup" #put your main folder path here

from pathlib import Path
from typing import List
from tqdm import tqdm

def get_developer_files(
    folder_path: str,
    allowed_extensions: List[str] = [".py", ".ipynb", ".txt" , ".md" , ".html" , ".js"]
) -> List[Path]:
    """
    Returns a list of developer-authored files in the given folder.

    Args:
        folder_path (str): The root directory to search.
        allowed_extensions (List[str], optional): File extensions to include. Defaults to [".py", ".ipynb", ".txt"].

    Returns:
        List[Path]: List of valid developer file paths.
    """
    folder = Path(folder_path).resolve()
    valid_files = []

    for path in tqdm(folder.rglob("*"), desc="Scanning developer files"):
        if not path.is_file():
            continue

        # Skip hidden files or folders (e.g., .git, .venv)
        if any(part.startswith(".") for part in path.parts):
            continue

        # Skip non-allowed extensions
        if path.suffix.lower() not in allowed_extensions:
            continue

        # Skip auto-generated or unnecessary files
        if "__pycache__" in path.parts or path.name == "__init__.py":
            continue

        valid_files.append(path)

    return valid_files
def save_to_markdown(content: str, filename: str = "output.md"):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Saved to {filename}")


def generate_prd(folder_path) :
    # import pdb; pdb.set_trace()
    files = get_developer_files(folder_path)
    print(files)
    summaries = []
    for one_file in tqdm(files) : 
        try:
                # import pdb; pdb.set_trace()
            with open(one_file, "r", encoding="utf-8") as f:
                content = f.read()
                response = client.responses.create(
                    model="gpt-4.1",
                    input=f"""You are a technical summarizer helping build documentation for a software project.
                        Below is the content of a file from the project (which may be code, documentation, or text notes).
                        Your task is to write a concise summary that explains the purpose and role of this file in the overall project.

                        Guidelines:

                        Focus on what the file does and why it exists.

                        Be specific, but brief — use professional and clear language.

                        If it's code, summarize the main functionality or classes/functions.

                        If it’s documentation (e.g. README), explain what it covers in detail.

                        If unsure, say what kind of content it appears to contain. Here is file content - {content} , file name - {one_file}

                        """
                                            )

                summaries.append(f"{one_file} : {response.output_text}")
        except Exception as e :
            print(e)
            continue
    # import pdb; pdb.set_trace()
    final_response = client.responses.create(
        model = "gpt-4.1",
        input = f"""You are a product manager analyzing a software codebase. Below is a list of 1–2 line summaries describing what each file in the repository does.
            Based on these summaries, write a detailed Product Requirements Document (PRD) that describes the software as if you were introducing it to a product and engineering team.

            Your PRD should include the following sections:

            Product Overview: A high-level summary of what the software does and its purpose.

            Core Features: List the main functionalities implemented across the codebase.

            Architecture Summary: Briefly describe how the project appears to be structured based on the files.

            Technology Stack: What technologies, frameworks, or libraries are likely in use?

            API or User Interface: If applicable, describe how the user or external systems interact with this software.

            Known Limitations / TODOs: Infer any areas that may still be under development or need improvement.

            Use professional, clear language, and ensure the document is easy to read for both technical and non-technical stakeholders.

            Here are the file summaries: {summaries}"""
        )
    
    print(final_response.output_text)
    save_to_markdown(final_response.output_text , 'output.md')
    return final_response


from pathlib import Path
from typing import List
import ast

# --- Keyword-based matching ---
DB_KEYWORDS = [
    "sqlalchemy", "create_engine", "declarative_base", "Column(", "ForeignKey(", "relationship(",
    "Base.metadata", "session.query", "session.add", "session.commit",
    "models.Model",  # Django
    "cursor.execute", "cursor.fetchone", "cursor.fetchall",
    "sqlite3.connect", "psycopg2.connect", "MySQLdb.connect",
    "create table", "insert into", "select * from"
]

def is_db_file(file_path: Path) -> bool:
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore").lower()
        return any(keyword in content for keyword in DB_KEYWORDS)
    except Exception:
        return False


# --- AST-based structure check (Python files only) ---
def uses_database_ast(file_path: Path) -> bool:
    try:
        tree = ast.parse(file_path.read_text(encoding="utf-8", errors="ignore"))
        for node in ast.walk(tree):
            # Check for relevant imports
            if isinstance(node, ast.ImportFrom):
                if node.module and ("sqlalchemy" in node.module or "django.db" in node.module):
                    return True

            # Check class inheritance
            if isinstance(node, ast.ClassDef):
                for base in node.bases:
                    if isinstance(base, ast.Name) and base.id in {"Base", "Model"}:
                        return True

            # Check function calls
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in {"create_engine", "connect", "Column", "execute"}:
                        return True
        return False
    except Exception:
        return False


# --- Combined DB module detector ---
def find_db_modules(
    folder_path: str,
    file_extensions: List[str] = [".py"]
) -> List[Path]:
    """
    Scans a folder for files containing database-related logic.

    Args:
        folder_path (str): The root directory to scan.
        file_extensions (List[str]): File types to consider (default: Python files only).

    Returns:
        List[Path]: List of file paths that likely contain DB-related code.
    """
    root = Path(folder_path).resolve()
    db_files = []

    for path in root.rglob("*"):
        if not path.is_file() or path.suffix not in file_extensions:
            continue
        if any(part.startswith(".") for part in path.parts):  # Skip hidden files/folders
            continue
        if is_db_file(path) or uses_database_ast(path):
            db_files.append(path)

    return db_files

def prepare_db_code_for_prompt(file_paths: list[Path]) -> str:
    prompt_input = ""

    for path in file_paths:
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            content = f"<Error reading file: {e}>"
        
        prompt_input += f"**{path.name}**\n```\n{content.strip()}\n```\n\n---\n\n"
    
    return prompt_input

db_prompt = """
You are a software architect analyzing a codebase to understand the structure of its database.

Below is a collection of code files that contain database-related logic. These files may include ORM models (e.g., SQLAlchemy, Django), raw SQL queries, or database access functions.

Your task is to review these files and generate a complete overview of the database, including both textual and visual documentation.

Your Output Must Include:
1. Database Schema

List all database tables found in the code.

For each table, list:

Field name

Data type

Constraints (e.g. primary key, foreign key, nullable, unique, default)

2. Entity Relationships

Identify relationships between tables (e.g. one-to-many, many-to-many).

Clearly state which fields define those relationships.

3. Database Usage Summary

Describe how the database is used in the code.

Note if ORM (e.g., SQLAlchemy, Django models) is used.

Highlight any raw SQL usage (e.g., cursor.execute(...), CREATE TABLE, etc.).

Mention any observed use of migrations, indexing, joins, or unusual patterns.

4. Mermaid ER Diagram

Generate a Mermaid ER diagram of the schema using erDiagram syntax.

Include all relevant tables and relationships.

Wrap the diagram in a Markdown code block so it can be rendered:

mermaid
Copy
Edit
erDiagram
  users {
    INT id PK
    STRING name
    STRING email
  }
  orders {
    INT id PK
    INT user_id FK
    FLOAT total
  }
  users ||--o{ orders : has
Input: Database-Related Code Files
(Each file is separated by ---)

{{filename_1}}

Copy
Edit
{{file_content_1}}
{{filename_2}}

Copy
Edit
{{file_content_2}}
(Continue for all files in your DB-related list)

✅ Output Format Example
markdown
Copy
Edit
## Database Schema

### Table: users
- id: Integer, Primary Key
- name: String, Not Null
- email: String, Unique

### Table: orders
- id: Integer, Primary Key
- user_id: Integer, Foreign Key → users.id
- total: Float

## Relationships
- One-to-many: users → orders via user_id

## Usage Summary
- SQLAlchemy is used to define models.
- Session-based queries for CRUD operations.
- No migrations or indexing detected.

## ER Diagram

```mermaid
erDiagram
  users {
    INT id PK
    STRING name
    STRING email
  }
  orders {
    INT id PK
    INT user_id FK
    FLOAT total
  }
  users ||--o{ orders : has
```
"""




def prd_main(path: Path):
    generate_prd(path)
    db_files = find_db_modules(path)
    code_lines = prepare_db_code_for_prompt(db_files)

    final_prompt = db_prompt + f"Below is a collection of code files that contain database-related logic...\n{code_lines}"

    resp = client.responses.create(
        model="gpt-4.1",
        input=final_prompt
    )

    with open("output.md", "a", encoding="utf-8") as f:
        f.write(resp.output_text)




