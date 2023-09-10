from . import views
from django.urls import path

from .views import CustomloginView, Task_and_Description_List,RegisterPage,EditTask
from django.contrib.auth.views import LogoutView 
urlpatterns = [
    
    
    path('login/', CustomloginView.as_view(), name='login'),
    path('registerPage/', RegisterPage.as_view(), name='registerPage'),
    path('', Task_and_Description_List.as_view(), name='home-todo'),
    path('logout/', LogoutView.as_view(next_page = 'login'), name='logout'),
    
    # # button to add a task 
    path('add_Task/', views.add_Task, name='add_Task'),
    
   
    # button to delete a task
    path('delete/<int:task_id>/', views.deleteTask, name='deleteTask'),
    # button to complete a task
    path('completeTask/<int:task_id>/', views.completeTask, name='completeTask'), 

    # button to clear completed tasks
    path('clearCompleted/', views.clearCompleted, name='clearCompleted'),

    # button to mark as undone tasks
    path('markAsUndone/<int:task_id>/', views.markAsUndone, name='markAsUndone'),
    
    # button to edit a task
    path('editTask/<int:pk>/', EditTask.as_view(), name='editTask'),

    # Delete all tasks
    path('deleteAll/', views.deleteAll, name='deleteAll'),
    path('showAddTask/', views.showAddTask, name='showAddTask'),



]