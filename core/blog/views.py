from django.shortcuts import render, HttpResponse
from .models import Blog


def home(request):
    blogs = Blog.objects.all()
    return render(request, 'blog/home.html', {'title': 'Hello Django', 'blogs': blogs})

def about(request):
    return render(request, 'blog/about.html')