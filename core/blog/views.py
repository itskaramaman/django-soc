from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Blog
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


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


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'description']
    template_name = 'blog/edit-blog.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin,  UserPassesTestMixin, UpdateView):
    model = Blog
    fields = ['title', 'description']
    template_name = 'blog/edit-blog.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self) -> bool | None:
        blog = self.get_object()
        return self.request.user == blog.author


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    success_url = '/'

    def test_func(self) -> bool | None:
        blog = self.get_object()
        return self.request.user == blog.author


def about(request):
    return render(request, 'blog/about.html')
