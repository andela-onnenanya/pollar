from django.forms import ModelForm
from .models import Choice, Poll, Vote
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    password1 = forms.CharField(widget=forms.PasswordInput(), help_text='Required. Use 8 or more characters')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class PollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ('title', 'description',)


class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = ('choice',)
