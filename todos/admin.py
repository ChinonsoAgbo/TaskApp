from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('task', 'is_completed', 'created_at') # display fields for Task model in admin panel
    search_fields = ('task',) # search fields for Task model in admin panel
# Register your models here.
admin.site.register(Task, TaskAdmin)