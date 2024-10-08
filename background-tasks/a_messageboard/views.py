from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from .tasks import *
from django.contrib import messages
import threading
from django.contrib.auth.decorators import user_passes_test
# Create your views here.
@login_required
def messageboard_view(request):
    messageboard = get_object_or_404(MessageBoard, id=1)
    form = MessageCreatedForm()
    if request.method == 'POST':
        if request.user in messageboard.subscribers.all():
            form = MessageCreatedForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.author = request.user
                message.messageboard = messageboard
                message.save()
                send_email(message)
        else:
            messages.warning(request, 'You need to be subscribed')
        return redirect('messageboard')

    context ={
        'messageboard': messageboard
        , 'form': form
    }
    return render(request, 'a_messageboard/index.html', context)

def subscribe(request):
    messageboard = get_object_or_404(MessageBoard, id=1)
    if request.user in messageboard.subscribers.all():
        messageboard.subscribers.remove(request.user)
    else:
        messageboard.subscribers.add(request.user)
    return redirect('messageboard')



def send_email(message):
    messageboard = message.messageboard
    subscribers = messageboard.subscribers.all()

    for subscriber in subscribers:
        subject = f"New Message from {message.author.profile.name}"
        body = f"{message.author.profile.name}: {message.body}\n\nRegards from\nMy Message Board"

        send_email_thread.delay(subject, body, subscriber.email)

def is_staff(user):
    return user.is_staff

@user_passes_test(is_staff)
def newsletter(request):
    return render(request, 'a_messageboard/newsletter.html')