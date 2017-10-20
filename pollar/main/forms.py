from django.forms import ModelForm
from .models import Choice, Poll, Vote

class PollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ('question',)

class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = ('choice',)

