from datetime import timedelta

from django import forms
from django.utils import timezone

from tinymce.widgets import TinyMCE

from .models import Letter, Comment


# Forms
class LetterForm(forms.ModelForm):
    
    class Meta:
        model = Letter
        fields = (
            'title',
            'content',
            'email_address',
            'delivery_date',
            'audience'
        )
        widgets = {'content': TinyMCE(attrs={'cols':75, 'rows': 30})}
       
    def clean_content(self):
        letter_content = self.cleaned_data['content']
        if not letter_content or letter_content == ' ':
            raise forms.ValidationError(r'Can\'t send empty letter.')
        return letter_content

    # def clean_delivery_date(self):
    #     date = self.cleaned_data['delivery_date']
    #     print(date)
    #     now = timezone.now().date()
    #     if date - now < timedelta(days=28):
    #         raise forms.ValidationError('Date should be at least a month from now.')
    #     return date


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('user', 'comment')
