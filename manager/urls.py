from django.urls import path

from .views import index, TaskListView, WorkersListView, TaskDetailView

urlpatterns = [
    path("", index, name="index"),
    path("tasks", TaskListView.as_view(), name="tasks"),
    path("tasks/<int:pk>", TaskDetailView.as_view(), name="task-detail"),
    path("workers", WorkersListView.as_view(), name="workers"),
]


app_name = "manager"