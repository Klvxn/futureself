from django.contrib import admin
from django.db import models

from tinymce.widgets import TinyMCE

from .models import Blog


# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'writer', 'date_posted')
    list_filter = ('writer', 'status')
    prepopulated_fields = {'slug':('title', )}
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }
    