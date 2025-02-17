from django.urls import path

from .views import index, TaskListView

urlpatterns = [
    path("", index, name="index"),
    path("tasks", TaskListView.as_view(), name="tasks"),
]


app_name = "manager"