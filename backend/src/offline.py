"""Module providing a langchain tool for table retriever."""
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.document_loaders import DirectoryLoader
from dotenv import load_dotenv

load_dotenv()

def store_table_schema_vector():
    """Load the document, split it into chunks, embed each chunk and load it into the vector store."""
    loader = DirectoryLoader("table-schema")
    documents = loader.load()
    db = FAISS.from_documents(documents, OpenAIEmbeddings())
    # return db.as_retriever(
    #     search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.5}
    # )
    db.save_local("weights")
    return 200

if __name__ == "__main__":
    store_table_schema_vector()
