from django.shortcuts import render
from django.http import HttpResponse
from .forms import PollForm, ChoiceForm, SignUpForm
from django.utils import timezone
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.http import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from .models import Choice, Poll, Vote

def login_user(request):
    if request.user.is_authenticated():
        return redirect('/')
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
    return render(request, 'user/login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def home(request):
    return render(request, 'main/index.html', {'greeting': 'Hi, How is coding going?'})

@login_required
def poll_new(request):
    if request.method == "POST":
        poll_form = PollForm(request.POST)
        choice_form = ChoiceForm(request.POST)
        if poll_form.is_valid() and choice_form.is_valid:
            poll = poll_form.save(commit=False)
            poll.author = request.user
            poll.save()
            poll_choices = choice_form.data['choice'].split(',')
            #Remove duplicates
            poll_choices = list(set(poll_choices))
            choice = choice_form.save(commit=False)
            for poll_choice in poll_choices:
                choice.pk = None
                choice.choice = poll_choice
                choice.poll = poll
                choice.vote = 0
                choice.save()
            return redirect('../.')
    else:
        poll_form = PollForm()
        choice_form = ChoiceForm()
    return render(request, 'snippets/add_poll.html', {'poll_form': poll_form, 'choice_form': choice_form})

@login_required
def polls(request):
    return render(request, 'poll/polls.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'user/signup.html', {'form': form})

def add_vote(request, poll_id):
        poll = Poll.objects.get(id=poll_id) 
        choice = Choice.objects.filter(poll=poll_id).order_by('id')
        if request.method == 'POST':
            vote = request.POST.get('choice')
            if vote:
                vote = Choice.objects.get(id=vote)  
                #saves the poll id, user id, and choice to the Votes table
                v = Votes(poll=poll, choiceVote = vote)
                v.save()
                #redirects the user to the results page after they submit their vote
                return redirect('../')