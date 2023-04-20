from django import forms

from .models import Blog


# Forms
class BlogForm(forms.ModelForm):
    
    class Meta:
        model = Blog
        fields = ('title', 'content', 'image')
