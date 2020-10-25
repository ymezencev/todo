from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
import logging


logger = logging.getLogger('auth')


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


def register_user(request):
    """Method fot user registration"""
    if request.user.is_authenticated:
        return redirect('todo')
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            logger.info(f'New user was registered. '
                f'Username: {username} user_id: {request.user.id}')
            return redirect('login')

    errors = form.errors.as_json()
    context = {
        'form': form,
        'errors': errors,
    }
    return render(request, 'todo/register.html', context)


def login_user(request):
    """Method for user login"""
    if request.user.is_authenticated:
        return redirect('todo')
    form = AuthenticationForm()
    errors = {}

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                logger.info(f'User logged in. '
                    f'Username: {username} user_id: {request.user.id}')
                return redirect('todo')

        errors = {'invalid_login': 'Incorrect username or password'}

    context = {
        'form': form,
        'errors': errors,
    }

    return render(request, 'todo/login.html', context)


def logout_user(request):
    """Method for user logout"""
    logger.info(f'User logged out. user_id: {request.user.id}')
    logout(request)
    return redirect('login')
