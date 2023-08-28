from django.urls import path

from . import views 
urlpatterns = [
    # button to add a task 
    path('addTask/', views.addTask, name='addTask'),
    # button to delete a task
    path('delete/<int:task_id>/', views.deleteTask, name='deleteTask'),
    # button to complete a task
    path('completeTask/<int:task_id>/', views.completeTask, name='completeTask'), # button to complete a task

    # button to clear completed tasks
    path('clearCompleted/', views.clearCompleted, name='clearCompleted'),

    # button to mark as undone tasks
    path('markAsUndone/<int:task_id>/', views.markAsUndone, name='markAsUndone'),
    
    # button to edit a task
    path('editTask/<int:task_id>/', views.editTask, name='editTask'),


]