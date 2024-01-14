from django.urls import path
from . import views

urlpatterns = [
    path('', views.BlogListView.as_view(), name="blog-home"),
    path('<int:pk>/', views.BlogDetailView.as_view(), name="blog"),
    path('about/', views.about, name="blog-about")
]
