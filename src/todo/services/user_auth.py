from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


def register_user(request):
    if request.user.is_authenticated:
        return redirect('todo')
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')

    errors = form.errors.as_json()
    context = {
        'form': form,
        'errors': errors,
    }
    return render(request, 'todo/register.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('todo')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('todo')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'todo/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')
