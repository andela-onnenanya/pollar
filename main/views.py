from django.shortcuts import render
from django.db import models
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
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
    print('USER', request.user)
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

def polls(request):
    all_polls = Poll.objects.all().order_by('date')
    if all_polls:
        first_poll = all_polls[0]
        first_poll_id = first_poll.id
        return redirect('/polls/' + str(first_poll_id))
    return render(request, 'poll/polls.html', {'polls': all_polls})

def trimString(word, number):
  if word:
    word = word
    return word
  else:
    return 'Chart Title'

def polls_view(request, poll_id):
    if request.method == 'GET':
        try:
            current_poll = Poll.objects.filter(id = poll_id)
            title = trimString(current_poll[0].title, 20)
        except NotImplementedError:
            return HttpResponse('No Poll Found with the specified id')
    all_polls = Poll.objects.all().order_by('date')
    options = Choice.objects.filter(poll=poll_id)
    return render(request, 'poll/polls.html', 
        {'title': title, 'polls': all_polls, 'options': options, 'current_poll': current_poll[0]}
        )

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

def votes(request, poll_id):
    poll = Poll.objects.get(id=poll_id) 
    if request.method == 'POST':
        choice_id = request.POST.get('choice')
        user = request.user
        can_vote = voter_check(request,user, poll)
        choice = Choice.objects.filter(poll=poll_id, id=choice_id)[0]
        if choice and can_vote['status'] == True:
            if request.user.is_authenticated:
                vote = Vote(poll=poll, choiceVote = choice, voter=user)
            else:
                vote = Vote(poll=poll, choiceVote = choice)
            vote.save()
            result = get_votes(poll_id)
            return JsonResponse({'votes': result, 'message':'Your vote has been submitted successfully!'})
        else:
            result = get_votes(poll_id)
            return JsonResponse({'votes':result, 'message':can_vote['message']})
    if request.method == 'GET':
        result = get_votes(poll_id)
        return JsonResponse({'votes': result})
        
def get_votes(poll_id):
    poll_votes = Vote.objects.filter(poll=poll_id).values('choiceVote').annotate(n=models.Count("pk"))
    poll_votes_flat = Vote.objects.filter(poll=poll_id).values_list('choiceVote', flat=True)
    choices = Choice.objects.filter(poll = poll_id).values('id', 'choice')
    result = []
    for choice in choices:
        name = choice['choice']
        choice_obj = {}
        choice_id = choice['id']
        for poll_vote in poll_votes:
            if poll_vote['choiceVote'] == choice_id:
                choice_obj['name'] = name
                choice_obj['vote'] = poll_vote['n']
                result.append(choice_obj)
        if choice_id not in poll_votes_flat:
            choice_obj['name'] = name
            choice_obj['vote'] = 0
            result.append(choice_obj)
        if len(poll_votes_flat) == 0:
            result = []
    print(result, poll_votes_flat)
    return result


def voter_check(request, user, poll):
    if not request.user.is_authenticated:
        return {'status':False, 'message':'Please sign in to vote!'}
    try:
        choice = Vote.objects.filter(poll=poll, voter=user)
    except TypeError:
        choice = []
    if len(choice) > 0:
        return {'status':False, 'message':'You have already voted and cannot vote again!' }
    return True


def about(request):
    if request.method == 'GET':
        return HttpResponse('Page under maintenance. Will be up in a 3 days time!')