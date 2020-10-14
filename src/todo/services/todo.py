from django.contrib.auth.models import User
from todo.models import Category, Task
from datetime import date


def get_categories(user_id: int):
    """Get all user categories"""
    categories = Category.objects.filter(user_id=user_id).order_by('order_num')
    return categories


def get_tasks(user_id: int, category_url: str):
    """Get user tasks consider passed category"""
    if category_url == 'all':
        tasks = get_all_tasks(user_id)
    elif category_url == 'important':
        tasks = get_important_tasks(user_id)
    elif category_url == 'my_day':
        tasks = get_my_day_tasks(user_id)
    else:
        tasks = get_custom_category_tasks(user_id, category_url)

    return tasks


def get_all_tasks(user_id: int):
    tasks = Task.objects.filter(user_id=user_id).order_by('-is_completed',
                                                          '-date_created')
    return tasks


def get_important_tasks(user_id: int):
    tasks = Task.objects.filter(
        user_id=user_id,
        is_important=True).order_by('-is_completed', '-date_created')

    return tasks


def get_my_day_tasks(user_id: int):
    today = date.today()
    tasks = Task.objects.filter(
        user_id=user_id,
        date_created__date=today).order_by('-is_completed', '-date_created')

    return tasks


def get_custom_category_tasks(user_id: int, category_url: str):

    tasks = Task.objects.filter(
        user=User.objects.get(id=user_id),
        category=Category.objects.get(url=category_url)).order_by(
            '-is_completed',
            '-date_created')

    return tasks


def add_task(user_id: int, text: str, category_url: str):
    """Add a user task with the specified category"""

    user = User.objects.get(id=user_id)
    # check if the task was created from the important tasks page
    is_important = True if category_url == 'important' else False

    task = Task.objects.create(task=text, is_important=is_important, user=user)

    category = Category.objects.filter(url=category_url, user=user)
    if category:
        task.category.add(*category)
