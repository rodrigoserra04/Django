from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Task
from .forms import TaskForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.http import JsonResponse
import json

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'todo/task_list.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
        else:
            print("Formulário inválido:", form.errors)
    else:
        form = TaskForm()
    return render(request, 'todo/add_task.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def homepage(request):
    return render(request, 'registration/homepage.html')

def kanban(request):
    tasks = Task.objects.all()
    
    todo_tasks = tasks.filter(status='ToDo')
    doing_tasks = tasks.filter(status='Doing')
    done_tasks = tasks.filter(status='Done')

    context = {
        'todo_tasks': todo_tasks,
        'doing_tasks': doing_tasks,
        'done_tasks': done_tasks,
    }
    return render(request, 'kanban/kanban.html', context)

def update_task_status(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.loads(request.body)
        print("data:", data)
        task_id = data['taskId']
        new_status = data['newStatus']
        print(task_id)
        
        try:
            # Obtenha a tarefa pelo ID
            task = Task.objects.get(pk=task_id)
            # Atualize o status da tarefa
            task.status = new_status
            task.save()

            # Após a atualização, busque todas as tarefas atualizadas
            todo_tasks = Task.objects.filter(status='ToDo')
            doing_tasks = Task.objects.filter(status='Doing')
            done_tasks = Task.objects.filter(status='Done')

            # Converta as consultas em dicionários
            todo_tasks_data = [{'id': task.id, 'title': task.title} for task in todo_tasks]
            doing_tasks_data = [{'id': task.id, 'title': task.title} for task in doing_tasks]
            done_tasks_data = [{'id': task.id, 'title': task.title} for task in done_tasks]

            # Retorne os dados atualizados em formato JSON
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
