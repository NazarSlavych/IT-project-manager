from django.urls import path

from .views import index, TaskListView, WorkersListView, TaskDetailView, WorkerDetailView, PositionsListView, \
    TaskTypeListView, WorkerCreateView, WorkerDeleteView, WorkerUpdateView

urlpatterns = [
    path("", index, name="index"),
    path("tasks", TaskListView.as_view(), name="tasks"),
    path("tasks/<int:pk>", TaskDetailView.as_view(), name="task-detail"),
    path("workers", WorkersListView.as_view(), name="workers"),
    path("workers/<int:pk>", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),
    path("workers/<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker-delete"),
    path("positions", PositionsListView.as_view(), name="positions"),
    path("tasktype", TaskTypeListView.as_view(), name="task-type"),
]


app_name = "manager"