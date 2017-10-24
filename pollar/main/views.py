from django.shortcuts import render
from django.http import HttpResponse
from .forms import PollForm, ChoiceForm
from django.shortcuts import redirect
from django.utils import timezone

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
