from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .services.user_auth import register_user, login_user, logout_user

def register_page(request):
    """Страница регистрации"""
    return register_user(request)

def login_page(request):
    """Страница входа в приложение"""
    return login_user(request)

def logout(request):
    """Выход из системы"""
    return logout_user(request)


@login_required
def todo(request):
    return render(request, 'todo/todo.html')
