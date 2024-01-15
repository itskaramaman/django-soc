from django.urls import path
from . import views

urlpatterns = [
    path('', views.BlogListView.as_view(), name="blog-home"),
    path('<int:pk>/', views.BlogDetailView.as_view(), name="blog"),
    path('create/', views.BlogCreateView.as_view(), name="blog-create"),
    path('update/<int:pk>/', views.BlogUpdateView.as_view(), name="blog-update"),
    path('delete/<int:pk>/', views.BlogDeleteView.as_view(), name="blog-delete"),
    path('about/', views.about, name="blog-about")
]
