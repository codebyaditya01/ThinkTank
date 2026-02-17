from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Questiondbase, Answerdbase, Commentdbase, Profiledbase

# Use built-in UserCreationForm
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username.lower() == 'admin':
            raise forms.ValidationError("Username cannot be 'admin'")
        return username

# Question form
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Questiondbase
        fields = ['title', 'body']
        widgets = {
            'body': forms.Textarea(attrs={'rows':3}),
        }

# Answer form
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answerdbase
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'rows':3}),
        }

# Comment form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Commentdbase
        fields = ['body']

# Profile form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profiledbase
        exclude = ['user', 'questions', 'answers']  # user is set in views
        # fields = '__all__' # Optional if you want all fields
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError("Please enter a valid Gmail address")
        return email
