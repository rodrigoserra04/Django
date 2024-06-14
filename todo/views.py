from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json, os
from .models import Task
from .forms import TaskForm
from .assistant.utils import get_ai_suggestions

@login_required
def task_list(request):
    tasks = Task.objects.order_by('-created_at')
    paginator = Paginator(tasks, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'todo/task_list.html', {'page_obj': page_obj})

def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'todo/task_detail.html', {'task': task})

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            print("PROMPT: ", request.POST)
            prompt = request.POST.get('description', '')
            if (os.getenv('OPEN_AI_ACTIVATED') == True):
                suggestions = get_ai_suggestions(prompt)
                task.ai_description = suggestions
            task.save()
            return redirect('task_list')
        else:
            print("Invalid Form:", form.errors)
    else:
        form = TaskForm()
    return render(request, 'todo/create_task.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
        
    for field in form.fields.values():
        field.help_text = None
    return render(request, 'registration/signup.html', {'form': form})

def homepage(request):
    return render(request, 'registration/homepage.html')

@login_required
def kanban(request):
    tasks = Task.objects.all()
    
    todo_tasks = tasks.filter(status='Pending')
    doing_tasks = tasks.filter(status='Doing')
    done_tasks = tasks.filter(status='Done')

    context = {
        'todo_tasks': todo_tasks,
        'doing_tasks': doing_tasks,
        'done_tasks': done_tasks,
    }
    return render(request, 'kanban/kanban.html', context)

@login_required
def update_task_status(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.loads(request.body)
        print("data:", data)
        task_id = data['taskId']
        new_status = data['newStatus']
        print(task_id)
        
        try:
            task = Task.objects.get(pk=task_id)
            task.status = new_status
            task.save()

            todo_tasks = Task.objects.filter(status='Pending')
            doing_tasks = Task.objects.filter(status='Doing')
            done_tasks = Task.objects.filter(status='Done')

            todo_tasks_data = [{'id': task.id, 'title': task.title} for task in todo_tasks]
            doing_tasks_data = [{'id': task.id, 'title': task.title} for task in doing_tasks]
            done_tasks_data = [{'id': task.id, 'title': task.title} for task in done_tasks]

            return JsonResponse({
                'todo_tasks': todo_tasks_data,
                'doing_tasks': doing_tasks_data,
                'done_tasks': done_tasks_data
            })
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
    
    return JsonResponse({'error': 'This endpoint only accepts AJAX requests'}, status=400)
        
class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)
