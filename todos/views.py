from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.views.generic.list import ListView
################# create a user and login that user after #############
from django.contrib.auth import login 

#################### django Authentication model ######################
from django.contrib.auth import login 
# Create your views here.
from django.urls import reverse_lazy 

############ restrict unregistered user  #########
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from todos.models import Task
from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required


#################### django Authentication model ######################
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm # to ccreate a user| and also the methodde fot login to log that user in. 
from django.views.generic.edit import UpdateView, FormView # FormView is to register a new user 

class CustomloginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    ########### move user afer loging in to task page 
    def get_success_url(self):
        return reverse_lazy('home-todo')


class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_autheticated_user = True
    success_url = reverse_lazy('home-todo')
    
    # varlidate the user 
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage,self).form_valid(form)
    # make sure that the already authenticated users cant see this register page 
    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home-todo')
        return super(RegisterPage,self).get(*args,**kwargs)
        
        
     
 ######## displaying tasks on home and ensure user kann only see there own data ############  
    
class Task_and_Description_List(LoginRequiredMixin,ListView):
    model = Task  # Model
    template_name = 'home-todo.html'
    context_object_name = 'tasks'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the queryset from the context or the default one if it doesn't exist
        tasks = context.get('tasks', Task.objects.all())

        # Filter the queryset based on the user attribute
        user = self.request.user
       # tasks = tasks.filter(user=user,is_completed=False)

        # Update the context with the filtered queryset and counts
        context['tasks_uncomplete'] = tasks.filter(user=user,is_completed=False).order_by('-created_at')
        context['tasks_complete'] = tasks.filter(user=user,is_completed=True).order_by('-created_at')
        context['count_completed'] =  context['tasks_uncomplete'].filter(is_completed=False).count()
        context['count_uncompleted'] =  context['tasks_complete'].filter(is_completed=True).count()

        ################# search logic ##################
        search_Info = self.request.GET.get('query') or ''
        
        if search_Info: #wenn der search gesucht wird! 
            # hier wird der suche mit der query angabe spezifich ausgefiltert 
            context['tasks_uncomplete'] = tasks.filter(user= user, task__startswith = search_Info,is_completed=False)
            context['tasks_complete'] = tasks.filter(user= user, task__startswith = search_Info,is_completed=True)
            context['count_completed'] =  context['tasks_uncomplete'].filter(is_completed=False).count()
            context['count_uncompleted'] =  context['tasks_complete'].filter(is_completed=True).count()


        return context
    
########### function view to add a new task ##############    
def add_Task(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            task = request.POST.get("task_title") # get task info 
            task_destcription = request.POST.get('task_details')
            if task :
                Task.objects.create(task=task,description=task_destcription, user = request.user)
            
    return redirect('home-todo')


def deleteTask(request, task_id):
    task = get_object_or_404(Task, id=task_id, user = request.user)  #
    task.delete()
    return redirect("home-todo")


# Mark a task as complete
def completeTask(request, task_id ):
    task = get_object_or_404(Task, id=task_id , user= request.user)  #
    task.is_completed = True
    if task.user == request.user:
            task.is_completed = True
            task.save()
    
    return redirect('home-todo')

# Mark a task as incomplete
def clearCompleted(request):
    Task.objects.filter(is_completed=True,user= request.user).delete()
    return redirect("home-todo")


# remark a task as incomplete

def markAsUndone(request, task_id):
    task = get_object_or_404(Task, id=task_id,user= request.user)  
    task.is_completed = False
    task.save()
    return redirect("home-todo")

# Edit an existing task
def editTask(request, task_id):
    get_task = get_object_or_404(Task, id=task_id,user= request.user)  
    if request.method == "POST":
        get_task.task = request.POST["task"]
        get_task.save()
        
      
        return JsonResponse({'success': True})  # Send a JSON response indicating success
    else:
        context = {"get_task": get_task}
        return render(request, "edit_task.html", context)
class EditTask(LoginRequiredMixin,UpdateView): # using class view to update task 
    model = Task
    fields = ['task','description']
    template_name = 'editTask.html'
    success_url = reverse_lazy('home-todo')
    
def deleteAll(request):
    tasks_to_delete = Task.objects.filter(user=request.user)
    tasks_to_delete.delete()
    return redirect("home-todo")

def showAddTask(request):
    return render(request, 'todoHeader.html')
