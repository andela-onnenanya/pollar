from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# class List(models.Model):
#     name = models.CharField(max_length=50)
#     description = models.CharField(max_length=50)
#     author = models.ForeignKey(User, related_name='poll_author')


class Poll(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    author = models.ForeignKey(User, related_name='poll_author', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.title, self.description)

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.TextField()

    class Meta:
        unique_together = (("choice", "poll"),)

    def __str__(self):
        return self.choice

class Vote(models.Model):
    poll = models.ForeignKey(Poll)
    choiceVote = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, null=True, default=User)

    class Meta:
        unique_together = (("poll", "voter"),)

    def __str__(self):
        return '%s %s %s' % (self.choiceVote, self.voter, self.poll)
