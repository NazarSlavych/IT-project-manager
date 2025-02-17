from django.urls import path

from .views import index, TaskListView

urlpatterns = [
    path("", index, name="index"),
    path("task", TaskListView.as_view(), name="tasks"),
]


app_name = "manager"