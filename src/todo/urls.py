from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout, name='logout'),

    path('', views.redirect_to_page_all_tasks, name='todo'),
    path('todo/', views.redirect_to_page_all_tasks, name='todo'),

    # categories
    path('todo/<slug:category_slug>/', views.get_todo_page, name='category'),

    path('todo/<slug:category_slug>/add_new_category',
         views.add_new_category,
         name='add_new_category'),
    path('todo/<slug:category_slug>/delete_category',
         views.delete_category,
         name='delete_category'),

    # tasks
    path('todo/<slug:category_slug>/add_new_task',
         views.add_new_task,
         name='add_new_task'),
    path('todo/<slug:category_slug>/delete_task',
         views.delete_task,
         name='delete_task'),
]
