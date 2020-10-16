from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.contrib.auth.models import User
from todo.models import Category
import hashlib


def create_category(name: str, user):
    """Base method to create a new category in the database"""

    name = get_new_unique_name(name, user)
    slug = get_new_slug(name, user)
    new_category = Category(name=name, user=user, slug=slug)
    new_category.save()

    return new_category

def update_category_name(new_name: str, category, user):
    name = get_new_unique_name(new_name, user)
    category.name = name
    category.slug = get_new_slug(name, user)
    category.save(update_fields=['name', 'slug'])

def update_category_order_num(new_order_num: int, category, user):
    pass

def delete_category(category):
    """Delete category"""
    category.delete()

def get_new_unique_name(name, user):
    """Get a new name until it is unique"""

    def is_name_unique(name, user):
        """check if there is no such category name yet"""
        category = Category.objects.filter(user=user, name=name)
        if category:
            return False
        return True
    def get_next_name(name, num):
        """get name + num:  MyCategory --> MyCategory (1)"""
        return f'{name} ({num})'

    _name = name
    _i = 1
    while not is_name_unique(name=name, user=user):
        name = get_next_name(name=_name, num=_i)
        _i += 1
    return name

def get_new_slug(name, user):
    user_category= str(user.id) + name
    slug =  hashlib.sha1((user_category).encode('utf-8')).hexdigest()
    return slug


def add_new_category(name: str, user_id: int):
    """Add a new custom user category  by user_id"""
    user = User.objects.get(id=user_id)
    category =  create_category(name=name, user=user)
    return category

def get_categories(user_id: int):
    """Get all user categories"""
    categories = Category.objects.filter(user_id=user_id).order_by('order_num')
    return categories