from django.shortcuts import render
from .models import *
# Create your views here.
def home(request):
    posts = Post.objects.all()
    return render(request, 'a_posts/home.html', {"posts": posts})


def post_create_view(request):
    return render(request, 'a_posts/post_create.html')