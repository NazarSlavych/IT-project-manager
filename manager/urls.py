from django.urls import path

from .views import index, TaskListView, WorkersListView



urlpatterns = [
    path("", index, name="index"),
    path("tasks", TaskListView.as_view(), name="tasks"),
    path("workers", WorkersListView.as_view(), name="workers"),
]


app_name = "manager"