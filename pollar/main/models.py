from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# class List(models.Model):
#     name = models.CharField(max_length=50)
#     description = models.CharField(max_length=50)
#     author = models.ForeignKey(User, related_name='poll_author')

class Poll(models.Model):
    question = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.choice

class Vote(models.Model):
    poll = models.ForeignKey(Poll)
    choiceVote = models.ForeignKey(Choice)
    
    def __str__(self):
        return self.choiceVote
