from django.db import models
from pgvector.django import VectorField
from .services import get_embedding
from decouple import config

EMBEDDING_LENGTH = config("EMBEDDING_LENGTH", default=3072, cast=int)
EMBEDDING_MODEL = "gemini-embedding-exp-03-07"


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    _content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    embedding = VectorField(dimensions=EMBEDDING_LENGTH, blank=True, null=True)
    can_delete = models.BooleanField(default=False, help_text="Use in jupyter notebook")


    def save(self, *args, **kwargs):
        has_changed = False
        if self._content != self.content:
            has_changed = True
            self._content = self.content

        if (self.embedding is None) or has_changed is True:
            # Generate embedding only if it doesn't exist
            raw_embedding_text = self.get_embedding_text_raw()
            if raw_embedding_text is not None:
                self.embedding = get_embedding(raw_embedding_text)
        super().save(*args, **kwargs)

    def get_embedding_text_raw(self):
        return self.content
    
    def embedding_length(self):
        return len(self.embedding) if self.embedding is not None else 0
