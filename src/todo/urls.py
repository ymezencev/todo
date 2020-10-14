from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout, name='logout'),

    path('', views.redirect_to_page_all_tasks, name='todo'), # redirect to all
    path('todo/', views.redirect_to_page_all_tasks, name='todo'), # redirect to all

    path('todo/<slug:category_url>/', views.get_todo_page, name='category'),
    path('todo/<slug:category_url>/add_new_task', views.add_new_task, name='add_new_task')
]
