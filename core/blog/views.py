from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.postgres.search import SearchQuery, SearchVector
from .models import Blog, BlogLike
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

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['liked'] = BlogLike.objects.filter(
            blog=context['blog'],
            user=self.request.user
        ).first()
        return context


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


def search(request):
    if request.method == 'POST':
        search_query = request.POST.get('search-query')
        if search_query:
            vector = SearchVector('title', weight='A') + \
                     SearchVector('description', weight='B')
            query = SearchQuery(search_query)
            hits = Blog.objects.annotate(search=vector).filter(search=query)
        return render(request, 'blog/home.html', {'blogs': hits})
    return render(request, 'blog/about.html')


@login_required
def blog_like_update(request):
    if request.method == 'POST':
        blog_id = request.POST.get('blog_id')
        blog = get_object_or_404(Blog, id=blog_id)
        liked = False
        # check if blog like exists
        blog_like = BlogLike.objects.filter(
            blog=blog,
            user=request.user
        ).first()

        if blog_like:
            blog_like.delete()
        else:
            BlogLike.objects.create(blog=blog, user=request.user)
            liked = True

        return render(request, 'blog/blog.html', {"blog": blog, "liked": liked})

    return redirect('/')


def about(request):
    return render(request, 'blog/about.html')
