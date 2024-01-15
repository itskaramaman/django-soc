from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Blog(models.Model):
    title = models.CharField(max_length=250, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog', kwargs={'pk': self.pk})
