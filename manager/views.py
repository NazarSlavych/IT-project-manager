from django.db.models import Count
from django.shortcuts import render

from manager.models import Task, Worker


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
