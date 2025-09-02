import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define the embedding model
# Always check the latest Google AI documentation for the recommended embedding model
EMBEDDING_MODEL = "models/text-embedding-004" # Or the latest recommended model

def get_embedding(text):
    """Generates an embedding for a given text."""
    try:
        response = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=text,
            task_type="retrieval_query" # Or "document" depending on your use case
        )
        # The embedding is usually in a list within the 'embedding' field
        return response['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

# Example Usage
text_to_embed_1 = "The quick brown fox jumps over the lazy dog."
text_to_embed_2 = "Artificial intelligence is transforming many industries."
text_to_embed_3 = "The cat sat on the mat."

embedding_1 = get_embedding(text_to_embed_1)
embedding_2 = get_embedding(text_to_embed_2)
embedding_3 = get_embedding(text_to_embed_3)

if embedding_1:
    print(f"Embedding for '{text_to_embed_1[:30]}...':")
    print(embedding_1[:5]) # Print first 5 dimensions for brevity
    print(f"Length: {len(embedding_1)}")

if embedding_2:
    print(f"\nEmbedding for '{text_to_embed_2[:30]}...':")
    print(embedding_2[:5])
    print(f"Length: {len(embedding_2)}")

if embedding_3:
    print(f"\nEmbedding for '{text_to_embed_3[:30]}...':")
    print(embedding_3[:5])
    print(f"Length: {len(embedding_3)}")