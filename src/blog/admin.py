from django.contrib import admin

from .models import BlogPost


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "timestamp", "embedding_length")
    search_fields = ("title", "content")
    list_filter = ("timestamp",)
    ordering = ("-timestamp",)
    date_hierarchy = "timestamp"


admin.site.register(BlogPost, BlogPostAdmin)
