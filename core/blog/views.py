from typing import Any
from django.shortcuts import render
from .models import Blog
from django.views.generic import ListView, DetailView


def home(request):
    blogs = Blog.objects.all()
    return render(request, 'blog/home.html', {'title': 'Hello Django', 'blogs': blogs})


class BlogListView(ListView):
    model = Blog
    template_name = "blog/home.html"  # <app>/<model>_<viewtype>.html
    context_object_name = 'blogs'
    ordering = ['-created_at']


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog.html'


def blog(request, id):
    blog = Blog.objects.filter(id=id)
    return render(request, 'blog/home.html', {'blogs': blog})


def about(request):
    return render(request, 'blog/about.html')
