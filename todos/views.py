from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q


from .models import Task

# Add a new task
def addTask(request):
    if request.method == "POST":
        task = request.POST.get("task")
        if task:
            Task.objects.create(task=task)
            return JsonResponse({"success": True})
    return JsonResponse({"success": False})


def deleteTask(request, task_id):
    task = get_object_or_404(Task, id=task_id)  #
    task.delete()
    return redirect("home-todo")


# Mark a task as complete
def completeTask(request, task_id):
    task = get_object_or_404(Task, id=task_id)  #
    task.is_completed = True
    task.save()
    return redirect("home-todo")


# Mark a task as incomplete
def clearCompleted(request):
    Task.objects.filter(is_completed=True).delete()
    return redirect("home-todo")


# remark a task as incomplete
def markAsUndone(request, task_id):
    task = get_object_or_404(Task, id=task_id)  
    task.is_completed = False
    task.save()
    return redirect("home-todo")


# Edit an existing task
def editTask(request, task_id):
    get_task = get_object_or_404(Task, id=task_id)  
    if request.method == "POST":
        get_task.task = request.POST["task"]
        get_task.save()
        return redirect("home-todo")
    else:
        context = {"get_task": get_task}
        return render(request, "edit_task.html", context)


def deleteAll(request):
    Task.objects.all().delete()
    return redirect("home-todo")



def searchBlogs(request):
    if'query' in request.GET and request.GET["query"]:
        search_term = request.GET.get("query")
        searched_blogs = Task.objects.filter(Q(task__icontains=search_term))# searches for the task
        message =  f'Search results for: {search_term}'

        # return Task.objects.filter(title__icontains=search_term)
        context = {
            'searched_blogs': searched_blogs,
            'message': message,
            'search_term': search_term,
        }
        return render(request, 'search.html', context)

    return render(request, 'search.html','no Info found ')  # Render 