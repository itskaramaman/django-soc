from django.shortcuts import render, HttpResponse
from .models import Blog


def home(request):
    blogs = Blog.objects.all()
    return render(request, 'blog/home.html', {'title': 'Hello Django', 'blogs': blogs})

def blog(request, id):
    blog = Blog.objects.filter(id=id)
    return render(request, 'blog/home.html', {'blogs': blog})

def about(request):
    return render(request, 'blog/about.html')