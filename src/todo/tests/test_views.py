from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.contrib.auth.models import User
from todo.models import Category
import json

from todo import views
from todo.services import todo_category, todo_task


class TestUserAuth(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.todo_utl = reverse('todo')
        self.category_all_url = reverse('category', args=('all',))

        self.register_data = {
            'username': 'user',
            'email': 'user@email.ru',
            'password1': 'secretStrongPass123',
            'password2': 'secretStrongPass123',
        }
        self.login_data = {
            'username': self.register_data['username'],
            'password': self.register_data['password1'],
        }

    # Login tests
    def test_redirect_after_login_success(self):
        response = self.client.post(self.register_url, self.register_data)
        self.assertRedirects(response, self.login_url)
        response = self.client.post(self.login_url, self.login_data, follow=True)
        self.assertRedirects(response, self.category_all_url, status_code=302, target_status_code=200)

    def test_redirect_after_login_failure(self):
        login_data_with_error  = dict.fromkeys(iter(self.login_data.keys()), 'error')
        response = self.client.post(self.login_url, login_data_with_error, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/login.html')

    def test_incorrect_password_login_failure(self):
        login_data_incorrect_password = self.login_data
        login_data_incorrect_password['password'] = 'error'
        response = self.client.post(self.register_url, self.register_data)
        self.assertRedirects(response, self.login_url)
        response = self.client.post(self.login_url, login_data_incorrect_password)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/login.html')
        login_error_msg = response.context['errors']
        self.assertNotEquals(login_error_msg, {})

    def test_user_doesnt_exist_login_failure(self):
        response = self.client.post(self.login_url, self.login_data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/login.html')
        login_error_msg = response.context['errors']
        self.assertNotEquals(login_error_msg, {})

    def test_redirect_to_todo_if_user_is_authorized(self):
        response = self.client.post(self.register_url, self.register_data)
        self.assertRedirects(response, self.login_url)
        response = self.client.post(self.login_url, self.login_data, follow=True)
        self.assertRedirects(response, self.category_all_url, status_code=302, target_status_code=200)
        response = self.client.post(self.login_url, self.login_data, follow=True)
        self.assertIn('_auth_user_id', self.client.session)
        self.assertTemplateUsed(response, 'todo/todo.html')

    # Register tests

    def test_redirect_to_login_after_registration_success(self):
        response = self.client.post(self.register_url, self.register_data)
        self.assertRedirects(response, self.login_url)

    def test_redirect_to_login_after_registration_failure(self):
        register_error_data = dict.fromkeys(iter(self.register_data.keys()), 'error')
        response = self.client.post(self.register_url, register_error_data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/register.html')

    def test_user_exists_register_failure(self):
        response = self.client.post(self.register_url, self.register_data)
        self.assertRedirects(response, self.login_url)
        response = self.client.post(self.register_url, self.register_data)
        user_error_msg = json.loads(response.context['errors'])['username'][0]['message']
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/register.html')
        self.assertEquals(user_error_msg, 'A user with that username already exists.')

    def test_passwords_dont_match_registration_failure(self):
        register_data_passwords_dont_match = self.register_data
        register_data_passwords_dont_match['password2'] = 'error'
        response = self.client.post(self.register_url, register_data_passwords_dont_match)
        reg_error_msg = json.loads(response.context['errors'])
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/register.html')
        self.assertNotEquals(reg_error_msg, {})

    def test_password_is_too_simple_registration_failure(self):
        simple_passwords = ['12345678', 'qwerty', 'qazwsxedc']
        for password in simple_passwords:
            self.register_data['password1'] = self.register_data['password2'] = password
            response = self.client.post(self.register_url, self.register_data)
            reg_error_msg = json.loads(response.context['errors'])
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'todo/register.html')
            self.assertNotEquals(reg_error_msg, {})


class TestTodoCategory(TestCase):

    def setUp(self):
        self.client = Client()
        self.category_all_url = reverse('category', args=('all',))
        self.user = User(username='user123', email='123@hello.ru')
        self.user.set_password('secretStrongPass123')
        self.user.save()
        self.client.login(username=self.user.username, password='secretStrongPass123')


    def test_get_zero_categories(self):
        categories = todo_category.get_categories(user_id=self.user.pk)
        self.assertEquals(categories.count(), 0)

    def test_get_categories(self):
        cat_one = todo_category.create_category('cat_one', user=self.user)
        cat_two = todo_category.create_category('cat_two', user=self.user)
        cat_three = todo_category.create_category('cat_three', user=self.user)
        categories = todo_category.get_categories(user_id=self.user.pk)
        self.assertNotEquals(categories.count(), 0)
        self.assertEquals(len(categories), 3)

    def test_get_categories_user_not_exists(self):
        categories = todo_category.get_categories(user_id=0)
        self.assertEquals(categories.count(), 0)

    def test_add_new_category_created_post(self):
        data = {'new_category': 'new_category_name'}
        add_new_category_url = reverse('add_new_category', args=('all',))
        response = self.client.post(add_new_category_url, data, follow=True)
        self.assertEquals(response.status_code, 200)
        categories = todo_category.get_categories(user_id=self.user.id)
        self.assertEquals(categories.count(), 1)

    def test_add_new_category_empty_name(self):
        data = {'new_category': ''}
        add_new_category_url = reverse('add_new_category', args=('all',))
        response = self.client.post(add_new_category_url, data, follow=True)
        self.assertEquals(response.status_code, 200)
        categories = todo_category.get_categories(user_id=self.user.id)
        self.assertEquals(categories.count(), 0)

    def test_add_new_category_redirect_new_category_slug(self):
        data = {'new_category': 'new_category_name'}
        add_new_category_url = reverse('add_new_category', args=('all',))
        response = self.client.post(add_new_category_url, data, follow=True)
        self.assertEquals(response.status_code, 200)
        new_category = todo_category.get_categories(user_id=self.user.id)[0]
        self.assertEquals(new_category.name, 'new_category_name')
        custom_slug_url = reverse('category', args=[new_category.slug])
        self.assertRedirects(response, custom_slug_url, status_code=302, target_status_code=200)

    def test_add_new_category_created_method(self):
        cat = todo_category.add_new_category(name='test_category', user_id=self.user.id)
        categories = todo_category.get_categories(user_id=self.user.id)
        self.assertEquals(categories.count(), 1)

    def test_add_new_category_invalid_user_method(self):
        cat = todo_category.add_new_category(name='test_category', user_id=777)
        categories = todo_category.get_categories(user_id=self.user.id)
        self.assertEquals(categories.count(), 0)

    def test_delete_category_by_slug(self):
        cat = todo_category.add_new_category(name='test_category', user_id=self.user.id)
        todo_category.delete_category_by_slug(cat.slug, user_id=self.user.id)
        categories = todo_category.get_categories(user_id=self.user.id)
        self.assertEquals(categories.count(), 0)

    def test_delete_category_by_slug_not_valid_user(self):
        cat = todo_category.add_new_category(name='test_category', user_id=self.user.id)
        todo_category.delete_category_by_slug(cat.slug, user_id=777)
        categories = todo_category.get_categories(user_id=self.user.id)
        self.assertEquals(categories.count(), 1)

    def test_delete_category_by_slug_category_does_not_exist(self):
        todo_category.delete_category_by_slug('no_such_category_slug', user_id=self.user.id)
        categories = todo_category.get_categories(user_id=self.user.id)
        self.assertEquals(categories.count(), 0)

    def test_go_to_custom_category_slug_url(self):
        cat = todo_category.add_new_category(name='test_category', user_id=self.user.id)
        cat_custom_url = reverse('category', args=[cat.slug])
        response = self.client.get(cat_custom_url, follow=True)
        self.assertEquals(response.status_code, 200)

    def test_delete_category_get(self):
        data = {'new_category': 'category_to_delete'}
        add_new_category_url = reverse('add_new_category', args=('all',))
        response = self.client.post(add_new_category_url, data, follow=True)
        self.assertEquals(response.status_code, 200)
        category_to_delete = todo_category.get_categories(user_id=self.user.id)[0]

        delete_category_url = reverse('delete_category', args=[category_to_delete.slug])
        response = self.client.get(delete_category_url, follow=True)
        self.assertEquals(response.status_code, 200)
        categories = todo_category.get_categories(user_id=self.user.id)
        self.assertEquals(categories.count(), 0)
        self.assertRedirects(response, self.category_all_url, status_code=302, target_status_code=200)

class TestTodoTask(TestCase):

    def setUp(self):
        self.client = Client()
        self.category_all_url = reverse('category', args=('all',))
        self.add_new_task = reverse('add_new_task', args=('all',))
        self.user = User(username='user123', email='123@hello.ru')
        self.user.set_password('secretStrongPass123')
        self.user.save()
        self.client.login(username=self.user.username, password='secretStrongPass123')

    def test_category_all_add_task(self):
        data = {'new_task': 'some text about the task'}
        response = self.client.post(self.add_new_task, data=data, follow=True)
        tasks = todo_task.get_all_tasks(self.user.id)
        self.assertEquals(tasks.count(), 1)
        self.assertEquals(tasks[0].task, 'some text about the task')
        self.assertRedirects(response, self.category_all_url, status_code=302, target_status_code=200)

    def test_category_important_add_task(self):
        data = {'new_task': 'some text about the task'}
        add_important_task = reverse('add_new_task', args=['important'])
        response = self.client.post(add_important_task, data=data, follow=True)
        tasks = todo_task.get_all_tasks(self.user.id)
        self.assertEquals(tasks.count(), 1)
        self.assertTrue(tasks[0].is_important)
        self.assertEquals(tasks[0].task, 'some text about the task')
        important_url = reverse('category', args=['important'])
        self.assertRedirects(response, important_url, status_code=302, target_status_code=200)

    def test_custom_category_add_task(self):
        custom_category = todo_category.create_category('custom_category', user=self.user)
        data = {'new_task': 'custom category task'}
        add_custom_task = reverse('add_new_task', args=[custom_category.slug])
        response = self.client.post(add_custom_task, data=data, follow=True)
        tasks = todo_task.get_all_tasks(self.user.id)
        self.assertEquals(tasks.count(), 1)
        self.assertEquals(tasks[0].task, 'custom category task')
        custom_category_url = reverse('category', args=[custom_category.slug])
        self.assertRedirects(response, custom_category_url, status_code=302, target_status_code=200)

    def test_add_empty_task(self):
        data = {'new_task': ''}
        response = self.client.post(self.add_new_task, data=data, follow=True)
        tasks = todo_task.get_all_tasks(self.user.id)
        self.assertEquals(tasks.count(), 0)
        self.assertRedirects(response, self.category_all_url, status_code=302, target_status_code=200)

    def test_add_task_more_than_400_characters(self):
        data = {'new_task': 'i'*401}
        response = self.client.post(self.add_new_task, data=data, follow=True)
        tasks = todo_task.get_all_tasks(self.user.id)
        self.assertEquals(tasks.count(), 1)
        self.assertEquals(len(tasks[0].task), 400)
        self.assertRedirects(response, self.category_all_url, status_code=302, target_status_code=200)

    def test_add_task_method_invalid_user(self):
        new_task = todo_task.add_task(text='new task', category_slug='all', user_id=0)
        self.assertIsNone(new_task)

    def test_add_task_method_category_not_exists(self):
        new_task = todo_task.add_task(text='new task', category_slug='not_exist', user_id=self.user.id)
        self.assertIsNone(new_task)


    def test_finish_task(self):
        data = {'new_task': 'new task text'}
        response = self.client.post(self.add_new_task, data=data, follow=True)
        tasks = todo_task.get_all_tasks(self.user.id)
        finish_task_url = reverse('finish_task', args=['all', tasks[0].id,])
        response = self.client.get(finish_task_url, follow=True)
        tasks = todo_task.get_all_tasks(self.user.id)
        self.assertEquals(tasks.count(), 1)
        self.assertTrue(tasks[0].is_completed)
        self.assertRedirects(response, self.category_all_url, status_code=302, target_status_code=200)

    def test_finish_task_when_task_not_exist(self):
        finish_task_url = reverse('finish_task', args=['all', 777,])
        response = self.client.get(finish_task_url, follow=True)
        tasks = todo_task.get_all_tasks(self.user.id)
        self.assertEquals(tasks.count(), 0)
        self.assertRedirects(response, self.category_all_url, status_code=302, target_status_code=200)

    def test_finish_task_category_not_exist(self):
        data = {'new_task': 'new task text'}
        response = self.client.post(self.add_new_task, data=data, follow=True)
        tasks = todo_task.get_all_tasks(self.user.id)
        finish_task_url = reverse('finish_task', args=['not_exist', tasks[0].id, ])
        try:
            response = self.client.get(finish_task_url, follow=True)
        except ObjectDoesNotExist:
            pass
        tasks = todo_task.get_all_tasks(self.user.id)
        self.assertEquals(tasks.count(), 1)
        self.assertTrue(tasks[0].is_completed)
        self.assertRedirects(response, self.category_all_url, status_code=302, target_status_code=200)

    def test_finish_task_pass_already_completed_task(self):
        data = {'new_task': 'new task text'}
        response = self.client.post(self.add_new_task, data=data, follow=True)
        tasks = todo_task.get_all_tasks(self.user.id)
        finish_task_url = reverse('finish_task', args=['all', tasks[0].id,])
        response = self.client.get(finish_task_url, follow=True)
        tasks = todo_task.get_all_tasks(self.user.id)
        self.assertEquals(tasks.count(), 1)
        self.assertTrue(tasks[0].is_completed)
        self.assertRedirects(response, self.category_all_url, status_code=302, target_status_code=200)

        response = self.client.get(finish_task_url, follow=True)
        self.assertEquals(tasks.count(), 1)
        self.assertTrue(tasks[0].is_completed)
        self.assertRedirects(response, self.category_all_url, status_code=302, target_status_code=200)

    def test_remove_from_completed(self):
        data = {'new_task': 'new task text'}
        response = self.client.post(self.add_new_task, data=data, follow=True)
        tasks = todo_task.get_all_tasks(self.user.id)
        finish_task_url = reverse('finish_task', args=['all', tasks[0].id,])
        response = self.client.get(finish_task_url, follow=True)
        tasks = todo_task.get_all_tasks(self.user.id)

        remove_from_completed_task_url = reverse('remove_from_completed', args=['all', tasks[0].id,])
        response = self.client.get(remove_from_completed_task_url, follow=True)
        tasks = todo_task.get_all_tasks(self.user.id)
        self.assertEquals(tasks.count(), 1)
        self.assertFalse(tasks[0].is_completed)
        self.assertRedirects(response, self.category_all_url, status_code=302, target_status_code=200)

    def test_remove_from_completed_not_completed_task(self):
        data = {'new_task': 'new task text'}
        response = self.client.post(self.add_new_task, data=data, follow=True)
        tasks = todo_task.get_all_tasks(self.user.id)

        remove_from_completed_task_url = reverse('remove_from_completed', args=['all', tasks[0].id, ])
        response = self.client.get(remove_from_completed_task_url, follow=True)
        tasks = todo_task.get_all_tasks(self.user.id)
        self.assertEquals(tasks.count(), 1)
        self.assertFalse(tasks[0].is_completed)
        self.assertRedirects(response, self.category_all_url, status_code=302, target_status_code=200)

    def test_remove_from_completed_task_not_exist(self):
        remove_from_completed_task_url = reverse('remove_from_completed', args=['all', 777, ])
        response = self.client.get(remove_from_completed_task_url, follow=True)
        tasks = todo_task.get_all_tasks(self.user.id)
        self.assertEquals(tasks.count(), 0)
        self.assertRedirects(response, self.category_all_url, status_code=302, target_status_code=200)

    def test_remove_from_completed_category_not_exist(self):
        data = {'new_task': 'new task text'}
        response = self.client.post(self.add_new_task, data=data, follow=True)
        tasks = todo_task.get_all_tasks(self.user.id)
        finish_task_url = reverse('finish_task', args=['all', tasks[0].id, ])
        response = self.client.get(finish_task_url, follow=True)
        tasks = todo_task.get_all_tasks(self.user.id)

        remove_from_completed_task_url = reverse('remove_from_completed', args=['not_exist', tasks[0].id, ])
        try:
            response = self.client.get(remove_from_completed_task_url, follow=True)
        except ObjectDoesNotExist:
            pass
        tasks = todo_task.get_all_tasks(self.user.id)
        self.assertEquals(tasks.count(), 1)
        self.assertFalse(tasks[0].is_completed)
        self.assertRedirects(response, self.category_all_url, status_code=302, target_status_code=200)

    def test_delete_task(self):
        data = {'new_task': 'new task text'}
        response = self.client.post(self.add_new_task, data=data, follow=True)
        response = self.client.post(self.add_new_task, data=data, follow=True)
        response = self.client.post(self.add_new_task, data=data, follow=True)
        tasks = todo_task.get_all_tasks(self.user.id)

        delete_task_url = reverse('delete_task', args=['all', tasks[0].id, ])
        response = self.client.get(delete_task_url, follow=True)
        tasks = todo_task.get_all_tasks(self.user.id)
        self.assertEquals(tasks.count(), 2)
        self.assertRedirects(response, self.category_all_url, status_code=302, target_status_code=200)

    def test_delete_task_when_task_not_exist(self):
        data = {'new_task': 'new task text'}
        response = self.client.post(self.add_new_task, data=data, follow=True)
        task_not_exist_id = 777
        delete_task_url = reverse('delete_task', args=['all', task_not_exist_id, ])
        response = self.client.get(delete_task_url, follow=True)
        tasks = todo_task.get_all_tasks(self.user.id)
        self.assertEquals(tasks.count(), 1)
        self.assertRedirects(response, self.category_all_url, status_code=302, target_status_code=200)

    def test_set_task_important(self):
        data = {'new_task': 'new task text'}
        response = self.client.post(self.add_new_task, data=data, follow=True)
        tasks = todo_task.get_all_tasks(self.user.id)
        set_task_important_url = reverse('set_task_important', args=['all', tasks[0].id, ])
        response = self.client.get(set_task_important_url, follow=True)
        tasks = todo_task.get_all_tasks(self.user.id)
        self.assertEquals(tasks.count(), 1)
        self.assertTrue(tasks[0].is_important)
        self.assertRedirects(response, self.category_all_url, status_code=302, target_status_code=200)

    def test_set_task_not_important(self):
        data = {'new_task': 'new task text'}
        response = self.client.post(self.add_new_task, data=data, follow=True)
        tasks = todo_task.get_all_tasks(self.user.id)
        set_task_important_url = reverse('set_task_important', args=['all', tasks[0].id, ])
        response = self.client.get(set_task_important_url, follow=True)
        tasks = todo_task.get_all_tasks(self.user.id)
        self.assertEquals(tasks.count(), 1)
        self.assertTrue(tasks[0].is_important)
        self.assertRedirects(response, self.category_all_url, status_code=302, target_status_code=200)

        set_task_not_important_url = reverse('set_task_not_important', args=['all', tasks[0].id, ])
        response = self.client.get(set_task_not_important_url, follow=True)
        tasks = todo_task.get_all_tasks(self.user.id)
        self.assertEquals(tasks.count(), 1)
        self.assertFalse(tasks[0].is_important)
        self.assertRedirects(response, self.category_all_url, status_code=302, target_status_code=200)

