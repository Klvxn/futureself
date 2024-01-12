from django import forms

from tinymce.widgets import TinyMCE

from .models import Blog


# Forms
class BlogForm(forms.ModelForm):
    
    class Meta:
        model = Blog
        fields = ('title', 'content', 'image')
        widgets = {'content': TinyMCE()}
