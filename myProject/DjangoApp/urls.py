from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("register/", views.register, name='register'),
    path("login/", views.login_view, name='login'),
    path("logout/", views.logout_view, name='logout'),
    path("tasks/", views.tasks, name='tasks'),
    path("add_task",views.add_task, name='add_task'),
    path("tasks/<int:id>", views.delete_task, name='delete_task'),
    path("tasks/<int:id>/edit", views.edit_task, name='edit_task'),
    path('update_task_status/<int:id>/', views.update_task_status, name='update_task_status'),
    path('assign_task/<int:id>/', views.assign_task, name='assign_task'),
    # path('filter_tasks_By_Status/', views.TaskFilterByStatusForm, name='filter_tasks_By_Status'),
    # path('tasks/sorted_by_executor/', views.tasks_sorted_by_executor, name='tasks_sorted_by_executor'),
    # path('tasks/filter/', views.filter_tasks, name='filter_tasks'),
]
