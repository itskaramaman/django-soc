from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Blog
from django.contrib.auth.models import User
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
    paginate_by = 5


class UserBlogListView(ListView):
    model = Blog
    template_name = "blog/user-blogs.html"
    context_object_name = 'blogs'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Blog.objects.filter(author=user).order_by('-created_at')


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
