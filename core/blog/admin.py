from django.contrib import admin
from .models import Blog, BlogLike

# Register your models here.
admin.site.register(Blog)
admin.site.register(BlogLike)
