from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from todo import views
from todo.services import todo_category


class TestUserAuth(TestCase):

    def test_login_page_url_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, views.login_page)

    def test_register_page_url_resolves(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, views.register_page)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, views.logout)


class TestTodoCategory(TestCase):

    def test_main_categories_resolves(self):
        main_categories = ('all', 'important', 'my_day')
        for cat in main_categories:
            url = reverse('category', args=(cat,))
            self.assertEquals(resolve(url).func, views.get_todo_page)

    def test_custom_category_slug_resolves(self):
        user = User(username='user', password='123', email='123@hello.ru')
        user.save()
        category = todo_category.create_category(name='custom_category', user=user)
        url = reverse('category', args=(category.slug,))
        self.assertEquals(resolve(url).func, views.get_todo_page)


class TestTodoTask(SimpleTestCase):

    def test_redirect_to_page_all_tasks_resolves(self):
        url = reverse('todo')
        self.assertEquals(resolve(url).func, views.redirect_to_page_all_tasks)


