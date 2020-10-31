from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.models import User
import json

from todo import views
from todo.services import todo_category


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

    pass


class TestTodoTask(SimpleTestCase):

    pass

