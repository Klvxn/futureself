from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Forms
class SignUpForm(UserCreationForm):
    
    username = forms.CharField(max_length=15, min_length=4)
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        
    def clean_email(self):
        email = self.cleaned_data["email"]
        user_exists = User.objects.filter(email=email).exists()
        if user_exists:
            raise forms.ValidationError("User with that email address already exists")
        return email


class UpdateUserForm(forms.ModelForm):

    username = forms.CharField(max_length=15, min_length=4)

    class Meta:
        model = User
        fields = ("username", "email")
        
    def clean_email(self):
        email = self.cleaned_data["email"]
        user_exists = User.objects.filter(email=email).exclude(email=email).exists()
        if user_exists:
            raise forms.ValidationError("User with that email address already exists")
        return email
