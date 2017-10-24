from django.shortcuts import render
from django.http import HttpResponse
from .forms import PollForm, ChoiceForm, SignUpForm
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

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
    return render(request, 'user/signup.html')

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
