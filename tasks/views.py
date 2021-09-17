from django.db import models
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy

from .models import Task

# Create your views here.


class UserLogin(LoginView):
    template_name = 'tasks/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class UserSignUP(FormView):
    template_name = 'tasks/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            # the login method used here is imported. check from the imports above
            login(self.request, user)
        return super(UserSignUP, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(UserSignUP, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    # the template name can be overwritten and it's given in the format: app_name/template_name
    template_name = 'tasks/tasks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['incomplete_tasks'] = context['tasks'].filter(
            task_completed=False)
        search_result = self.request.GET.get('search-area') or ''
        if search_result:
            context['tasks'] = context['tasks'].filter(
                title__icontains=search_result)
        context['search_result'] = search_result
        return context


class TaskDetails(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'tasks/task_details.html'


class CreateTask(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'task_completed']
    success_url = reverse_lazy('tasks')
    template_name = 'tasks/form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTask, self).form_valid(form)


class UpdateTask(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'task_completed']
    success_url = reverse_lazy('tasks')
    template_name = 'tasks/form.html'


class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    template_name = 'tasks/delete.html'

# I used function-based view for this particular view becuase I didn't
# know how to implement that with a class-based view


def task_status(request, pk):
    selected_task = Task.objects.get(id=pk)
    if selected_task != None:
        if selected_task.task_completed == False:
            selected_task.task_completed = True
            selected_task.save()
            return redirect('tasks')
        else:
            selected_task.task_completed = False
            selected_task.save()
            return redirect('tasks')
    context = {
        'task': selected_task
    }
    return render(request, 'tasks/task_details.html', context)
