from django.contrib.auth.models import User
from todo.models import Category
import hashlib
import logging


logger = logging.getLogger(__name__)


def create_category(name: str, user):
    """Base method to create a new category in the database"""

    name = get_new_unique_name(name, user)
    slug = get_new_slug(name, user)
    new_category = Category(name=name, user=user, slug=slug)
    new_category.save()

    logger.debug(f'Category was created. '
        f'user_id: {user.id} category_id: {new_category.id}')

    return new_category

def update_category_name(new_name: str, category, user):
    name = get_new_unique_name(new_name, user)
    category.name = name
    category.slug = get_new_slug(name, user)
    category.save(update_fields=['name', 'slug'])

    logger.debug(f'Category name was updated. '
        f'user_id: {user.id} category_id: {category.id}')



def update_category_order_num(new_order_num: int, category, user):
    pass


def delete_category_by_slug(slug: str, user_id: int):
    """Delete user category by passed name"""
    user = User.objects.get(id=user_id)
    if user is None:
        logger.error(f'User not found. Can not delete a category. '
            f'user_id: {user_id} slug: {slug}')
        return

    category = Category.objects.filter(user=user, slug=slug)
    if category is None:
        logger.error(f'Category not found. Can not delete a category. '
           f'user_id: {user_id} slug: {slug}')
        return

    logger.debug(f'Delete a category. user_id: {user_id} slug: {slug}')

    category.delete()


def get_new_unique_name(name, user):
    """Get a new name until it is unique"""

    if user is None:
        logger.error(f'User not found when creating a new unique name '
            f'user: {user} category_name: {name}')
        return

    def is_name_unique(name, user):
        """check if there is no such category name yet"""
        category = Category.objects.filter(user=user, name=name)
        if category is not None:
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

    logger.debug(f'Get a new unique name for a category. '
        f'user_id: {user.id} name: {name}')
    return name


def get_new_slug(name, user):

    if user is None:
        logger.error(f'User not found when getting a new slug '
            f'user: {user} category_name: {name}')
        return

    user_category= str(user.id) + name
    slug =  hashlib.sha1((user_category).encode('utf-8')).hexdigest()

    logger.debug(f'Get a new slug for category. '
        f'user_id: {user.id} slug: {slug}')

    return slug


def add_new_category(name: str, user_id: int):
    """Add a new custom user category  by user_id"""
    user = User.objects.get(id=user_id)
    if user is None:
        logger.error(f'User not found. '
            f'user: {user_id} category_name: {name}')
        return

    category =  create_category(name=name, user=user)

    logger.debug(f'New category was added. '
        f'user_id: {user_id} category_id: {category.id}')
    return category

def get_categories(user_id: int):
    """Get all user categories"""
    categories = Category.objects.filter(user_id=user_id).order_by('order_num')

    if categories is None:
        logger.error(f'Categories not found. user: {user_id}')
        return
    logger.debug(f'get all categories for user_id: {user_id}')

    return categories
