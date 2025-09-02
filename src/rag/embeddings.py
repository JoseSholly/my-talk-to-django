from typing import List
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from google.genai.types import EmbedContentConfig
from decouple import config

EMBEDDING_MODEL = config("EMBEDDING_MODEL", default="gemini-embedding-exp-03-07")
EMBEDDING_LENGTH = config("EMBEDDING_LENGTH", default=3072, cast=int)
GEMINI_API_KEY = config("GEMINI_API_KEY", cast=str)

class MyGoogleGenAIEmbedding(GoogleGenAIEmbedding):
    def __init__(self, model_name, api_key):
        super().__init__(model_name=model_name, api_key=api_key, embedding_config = EmbedContentConfig(output_dimensionality=EMBEDDING_LENGTH))

    def _get_query_embedding(self, query: str) -> List[float]:
        return super()._get_query_embedding(query)

    def _get_text_embedding(self, text: str) -> List[float]:
        return super()._get_text_embedding(text)  # Remove [text] wrapping

    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        return super()._get_text_embeddings(texts)

embed_model = MyGoogleGenAIEmbedding(
    model_name=EMBEDDING_MODEL,
    api_key=GEMINI_API_KEY
)

