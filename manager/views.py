from django.db.models import Count
from django.shortcuts import render
from django.views import generic
from manager.models import Task, Worker, Position


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


class TaskListView(generic.ListView):
    model = Task
    context_object_name = "task_list"


class TaskDetailView(generic.DetailView):
    model = Task


class WorkersListView(generic.ListView):
    model = Worker
    context_object_name = "workers_list"
    template_name = "manager/workers_list.html"


class WorkerDetailView(generic.DetailView):
    model = Worker


class PositionsListView(generic.ListView):
    model = Position
