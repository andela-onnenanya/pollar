from django.shortcuts import render
from django.http import HttpResponse
from .forms import PollForm, ChoiceForm, SignUpForm
from django.utils import timezone
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.http import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

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

def poll_new(request):
    if request.method == "POST":
        form = PollForm(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.author = request.user
            poll.published_date = timezone.now()
            poll.save()
            return redirect('home')
    else:
        form = PollForm()
    return render(request, 'snippets/poll_edit.html', {'form': form})

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
