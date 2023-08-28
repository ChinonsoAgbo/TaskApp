from django.http import HttpResponse
from django.shortcuts import redirect,render,get_object_or_404

from .models import Task

# Add a new task
def addTask(request):
    task = request.POST['task'] # get HTTP POST data
    if task: # if task is not empty
        Task.objects.create(task=task) # create a new Task object
    return redirect('home-todo')

def deleteTask(request,task_id):
    task=get_object_or_404(Task,id=task_id) #
    task.delete()
    return redirect('home-todo')

# Mark a task as complete 
def completeTask(request,task_id):
    task=get_object_or_404(Task,id=task_id) #
    task.is_completed=True
    task.save()
    return redirect('home-todo')

# Mark a task as incomplete
def clearCompleted(request):
    Task.objects.filter(is_completed=True).delete()
    return redirect('home-todo')

#remark a task as incomplete
def markAsUndone(request,task_id):
    task=get_object_or_404(Task,id=task_id) #
    task.is_completed=False
    task.save()
    return redirect('home-todo')

# Edit an existing task
def editTask(request,task_id):
    get_task=get_object_or_404(Task,id=task_id) #
    if request.method == 'POST':
        get_task.task=request.POST['task']
        get_task.save()
        return redirect('home-todo')
    else:
        context = {'get_task':get_task}
        return render(request,'edit_task.html', context)