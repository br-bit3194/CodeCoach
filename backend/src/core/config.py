import os
from dataclasses import dataclass
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    OPENAI_EMBEDDINGS_MODEL: str
    OPENAI_MODEL_NAME: str
    OPENAI_MODEL_TEMPERATURE: float
    OPENAI_API_KEY: str
    DOC_RETRIEVAL_TOP_K: int

    class Config:
        env_file = ".env"
        extra = "ignore"
    
# Create an instance of Settings to load environment variables
settings = Settings()

# @dataclass
# class Settings:
#     OPENAI_EMBEDDINGS_MODEL: str
#     OPENAI_MODEL_NAME: str
#     OPENAI_MODEL_TEMPERATURE: float
#     OPENAI_API_KEY: str
#     DOC_RETRIEVAL_TOP_K: int

# # Create an instance of Settings to load environment variables
# settings = Settings(
#             OPENAI_EMBEDDINGS_MODEL = os.environ["OPENAI_EMBEDDINGS_MODEL"],
#             OPENAI_MODEL_NAME = os.environ["OPENAI_MODEL_NAME"],
#             OPENAI_MODEL_TEMPERATURE = os.environ["OPENAI_MODEL_TEMPERATURE"],
#             OPENAI_API_KEY = os.environ["OPENAI_API_KEY"],
#             DOC_RETRIEVAL_TOP_K = os.environ["DOC_RETRIEVAL_TOP_K"]
#         )