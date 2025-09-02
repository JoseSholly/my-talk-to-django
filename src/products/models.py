from django.db import models
from pgvector.django import VectorField
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from decouple import config
EMBEDDING_LENGTH = config("EMBEDDING_LENGTH", default=1536, cast=int)
EMBEDDING_MODEL = "gemini-embedding-exp-03-07"



class Embedding(models.Model):
    embedding = VectorField(dimensions=EMBEDDING_LENGTH, blank=True, null=True)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    content_object = GenericForeignKey("content_type", "object_id")


class Product(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    embedding_obj = GenericRelation(Embedding)
    can_delete = models.BooleanField(default=False, help_text="Use in jupyter notebook")

    def get_embedding_text_raw(self):
        return self.content
