from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from manager.forms import WorkerCreationForm, WorkerUpdateForm, TaskForm
from manager.models import Task, Worker, Position, TaskType


@login_required
def index(request):
    num_task = Task.objects.count()
    num_worker = Worker.objects.count()
    num_free_workers = Worker.objects.annotate(task_count=Count("workers")).filter(task_count=0).count()
    context = {
        "num_task": num_task,
        "num_worker": num_worker,
        "num_free_workers": num_free_workers,
    }
    return render(request, "manager/index.html", context)


class TaskListView(LoginRequiredMixin ,generic.ListView):
    model = Task
    context_object_name = "task_list"
    queryset = Task.objects.select_related("task_type")


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("manager:tasks")


class WorkersListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    context_object_name = "workers_list"
    template_name = "manager/workers_list.html"
    queryset = Worker.objects.select_related("position")


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("manager:workers")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("manager:workers")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("manager:workers")


class PositionsListView(LoginRequiredMixin, generic.ListView):
    model = Position


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
