from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # form.save()
            messages.success(
                request,
                'Your account has been created! You are now able to login'
            )
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    print(request.user.profile.image.url)
    return render(request, "users/profile.html")
