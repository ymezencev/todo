from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .services.user_auth import register_user, login_user, logout_user
from .services import todo

from datetime import date


def register_page(request):
    """Page for user registration"""
    return register_user(request)

def login_page(request):
    """Page for user login"""
    return login_user(request)

def logout(request):
    """Page for user logout"""
    return logout_user(request)


@login_required
def get_todo_page(request, category_url:str='all'):
    """ Render todo page:
        Get categories
        Get all tasks or get category_url tasks"""
    user_id = request.user.id
    today = date.today()
    categories = todo.get_categories(user_id=user_id)
    tasks = todo.get_tasks(user_id=user_id, category_url=category_url)

    context = {
        'today': today,
        'current_category_url': category_url,
        'categories': categories,
        'tasks': tasks,
    }
    return render(request, 'todo/todo.html', context)


@login_required
def redirect_to_page_all_tasks(request):
    category_url = 'all'
    url = reverse('category', args=(category_url,))
    return redirect(url)


@login_required
def add_new_task(request, category_url:str='all'):
    """Add a new task and go back to the todo page"""

    if request.method == 'POST':
        new_task = request.POST.get('new_task')
        if new_task is not None or new_task != '':
            # add a new task
            user_id = request.user.id
            todo.add_task(user_id=user_id, text=new_task, category_url=category_url)

        url = reverse('category', args=(category_url,))
        return redirect(url)
