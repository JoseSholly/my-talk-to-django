from google import genai
from google.genai import types
from decouple import config
from django.apps import apps
from pgvector.django import CosineDistance
from django.db.models import F
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
EMBEDDING_MODEL = config("EMBEDDING_MODEL", default="gemini-embedding-exp-03-07", cast=str)
EMBEDDING_LENGTH = config("EMBEDDING_LENGTH", default=3072, cast=int)

GEMINI_API_KEY = config("GEMINI_API_KEY", cast=str)


def get_embedding(text, task_type="retrieval_document"):
    """
    Generates an embedding for a given text using the Gemini API.
    Ensure GEMINI_API_KEY is set in your Django settings.
    """

    try:
        client = genai.Client(api_key=config("GEMINI_API_KEY"))
        response = client.models.embed_content(
            model="gemini-embedding-exp-03-07",
            contents=text,
            config=types.EmbedContentConfig(output_dimensionality=3072, task_type=task_type)
        )
        # Access the actual list of float values from the ContentEmbedding object
        if response.embeddings and len(response.embeddings) > 0:
            # response.embeddings is a list of ContentEmbedding objects
            # Each ContentEmbedding object has a 'values' attribute which is the list of floats
            return response.embeddings[0].values
        else:
            print("Warning: No embeddings found in the response.")
            return None

    except Exception as e:
        print(f"Error generating Gemini embedding: {e}")
        return None
    

def get_query_embedding(text):
    # get_or_create Query Embeddding model
    query_embedding = get_embedding(text)
    if query_embedding is None:
        raise ValueError("Failed to generate query embedding.")
    return query_embedding

    

def search_posts(query, limit=5):
    BlogPost = apps.get_model(app_label='blog', model_name='BlogPost')

    query_embedding = get_query_embedding(query)

    qs = BlogPost.objects.annotate(
        distance=CosineDistance('embedding',query_embedding),
        similarity=1 - F("distance")
    ).order_by("distance")[:limit]
    # for obj in qs: 
    #     print(obj.object_id, obj.content_object.id, obj.content_object.title, obj.distance, obj.similarity * 100)
    return qs