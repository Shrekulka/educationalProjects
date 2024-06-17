from typing import Any

from django.contrib import auth
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from users.forms import UserLoginForm


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username: Any = request.POST['username']
            password: Any = request.POST['password']
            user: AbstractBaseUser | None = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()

    context: dict[str, Any] = {
        'title': 'Home - Авторизация',
        'form': form,
    }
    return render(request, 'users/login.html', context)


def registration(request):
    context = {
        'title': 'Home - Регистрация',
    }
    return render(request, 'users/registration.html', context)


def profile(request):
    context = {
        'title': 'Home - Кабинет',
    }
    return render(request, 'users/profile.html', context)


def logout(request):
    pass

