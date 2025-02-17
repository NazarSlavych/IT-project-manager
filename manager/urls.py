from django.urls import path

from .views import index, TaskListView, WorkersListView, TaskDetailView, WorkerDetailView

urlpatterns = [
    path("", index, name="index"),
    path("tasks", TaskListView.as_view(), name="tasks"),
    path("tasks/<int:pk>", TaskDetailView.as_view(), name="task-detail"),
    path("workers", WorkersListView.as_view(), name="workers"),
    path("workers/<int:pk>", WorkerDetailView.as_view(), name="worker-detail"),
]


app_name = "manager"