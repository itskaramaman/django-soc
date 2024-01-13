from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="blog-home"),
    path('<int:id>/', views.blog, name="blog"),
    path('about/', views.about, name="blog-about")
]