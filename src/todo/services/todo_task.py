from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from todo.models import Category, Task
from datetime import date


def get_tasks(category_slug: str, user_id: int):
    """Get user tasks consider passed category"""
    if category_slug == 'all':
        tasks = get_all_tasks(user_id)
    elif category_slug == 'important':
        tasks = get_important_tasks(user_id)
    elif category_slug == 'my_day':
        tasks = get_my_day_tasks(user_id)
    else:
        tasks = get_custom_category_tasks(category_slug, user_id)

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


def get_custom_category_tasks(category_slug: str, user_id: int):

    tasks = Task.objects.filter(
        user=User.objects.get(id=user_id),
        category=Category.objects.get(slug=category_slug)).order_by(
            '-is_completed',
            '-date_created')

    return tasks


def add_task(text: str, category_slug: str, user_id: int):
    """Add a user task with the specified category"""

    user = User.objects.get(id=user_id)
    # check if the task was created from the important tasks page
    is_important = True if category_slug == 'important' else False

    task = Task.objects.create(task=text, is_important=is_important, user=user)

    category = Category.objects.filter(slug=category_slug, user=user)
    if category:
        task.category.add(*category)

    return task


def delete_task(task_id):
    """Delete task by id"""
    task = Task.objects.get(id=task_id)
    task.delete()

