from django.contrib import admin

from .models import Blog


# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'writer', 'date_posted')
    list_filter = ('writer', 'status')
    prepopulated_fields = {'slug':('title', )}
    