from decouple import config
from llama_index.llms.google_genai import GoogleGenAI

from llama_index.core import Settings

from .embeddings import MyGoogleGenAIEmbedding



EMBEDDING_MODEL = config("EMBEDDING_MODEL", default="gemini-embedding-exp-03-07")
EMBEDDING_LENGTH = config("EMBEDDING_LENGTH", default=3072, cast=int)
GEMINI_API_KEY = config("GEMINI_API_KEY", cast=str)
LLM_MODEL = config("LLM_MODEL", default="gemini-2.0-flash")

VECTOR_DB_NAME = config("VECTOR_DB_NAME", default='vector_db')
VECTOR_DB_TABLE_NAME = config("VECTOR_DB_TABLE_NAME", default='blogpost')

def init():
    llm = GoogleGenAI(model=LLM_MODEL, api_key=GEMINI_API_KEY)
    embed_model = MyGoogleGenAIEmbedding(model_name=EMBEDDING_MODEL, api_key=GEMINI_API_KEY)
    Settings.llm = llm
    Settings.embed_model = embed_model
