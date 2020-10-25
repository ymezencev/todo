from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from datetime import date

from .services.user_auth import register_user, login_user, logout_user
from .services import todo_task, todo_category


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
def get_todo_page(request, category_slug:str='all'):
    """ Render todo page:
        Get categories
        Get all tasks or get category_slug tasks"""
    user_id = request.user.id
    today = date.today()
    categories = todo_category.get_categories(user_id=user_id)
    tasks = todo_task.get_tasks(category_slug=category_slug, user_id=user_id)

    context = {
        'today': today,
        'current_category_slug': category_slug,
        'categories': categories,
        'tasks': tasks,
    }

    return render(request, 'todo/todo.html', context)


@login_required
def redirect_to_page_all_tasks(request):
    """Redirect to todo page (call get_todo_page)"""
    category_slug = 'all'
    url = reverse('category', args=(category_slug,))
    return redirect(url)


@login_required
def add_new_category(request, category_slug: str):
    """Add a new category and go to the todo page with this category"""

    if request.method == 'POST':
        new_category_name = request.POST.get('new_category')
        if new_category_name is not None and new_category_name != '':
            user_id = request.user.id
            new_category = todo_category.add_new_category(
                name=new_category_name,
                user_id=user_id,)
            category_slug = new_category.slug

        url = reverse('category', args=(category_slug,))
        return redirect(url)


@login_required
def delete_category(request, category_slug: str):
    """Delete category by slug"""
    if request.method == 'GET':
        user_id = request.user.id
        todo_category.delete_category_by_slug(slug=category_slug, user_id=user_id)

    url = reverse('category', args=('all',))
    return redirect(url)


@login_required
def add_new_task(request, category_slug: str):
    """Add a new task and go back to the todo page"""

    if request.method == 'POST':
        new_task_text = request.POST.get('new_task')
        if new_task_text is not None and new_task_text != '':
            # add a new task
            user_id = request.user.id
            new_task = todo_task.add_task(
                text=new_task_text,
                category_slug=category_slug,
                user_id=user_id,)

        url = reverse('category', args=(category_slug,))
        return redirect(url)


@login_required
def finish_task(request, category_slug: str, task_id: int):
    """Finish task and get back to passed category_slug page"""
    if request.method == 'GET':
        user_id = request.user.id
        todo_task.finish_task(task_id=task_id)

    url = reverse('category', args=(category_slug,))
    return redirect(url)


@login_required
def delete_task(request, category_slug: str, task_id: int):
    """Delete task and get back to passed category_slug page"""
    if request.method == 'GET':
        todo_task.delete_task(task_id=task_id)

    url = reverse('category', args=(category_slug,))
    return redirect(url)
