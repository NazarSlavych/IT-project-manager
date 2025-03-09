from django.urls import path

from manager.views import (
    index,
    WorkersListView,
    TaskDetailView,
    WorkerDetailView,
    PositionsListView,
    TaskTypeListView,
    WorkerCreateView,
    WorkerDeleteView,
    WorkerUpdateView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    TeamListView,
    TeamDetailView,
    TeamUpdateView,
    TeamDeleteView,
    toggle_assign_to_task,
    TeamCreateView,
    login_view,
)

urlpatterns = [
    path("", index, name="index"),
    path("tasks/<int:pk>", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path(
        "projects/<int:project_id>/tasks/create/",
        TaskCreateView.as_view(),
        name="task-create",
    ),
    path("workers", WorkersListView.as_view(), name="workers"),
    path("workers/<int:pk>", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),
    path("workers/<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker-delete"),
    path("projects/", ProjectListView.as_view(), name="projects"),
    path("projects/<int:pk>", ProjectDetailView.as_view(), name="project-detail"),
    path("projects/create/", ProjectCreateView.as_view(), name="project-create"),
    path(
        "projects/<int:pk>/update/", ProjectUpdateView.as_view(), name="project-update"
    ),
    path(
        "projects/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project-delete"
    ),
    path("teams/", TeamListView.as_view(), name="teams"),
    path("teams/<int:pk>", TeamDetailView.as_view(), name="team-detail"),
    path("teams/create/", TeamCreateView.as_view(), name="team-create"),
    path("teams/<int:pk>/update/", TeamUpdateView.as_view(), name="team-update"),
    path("teams/<int:pk>/delete/", TeamDeleteView.as_view(), name="team-delete"),
    path("positions", PositionsListView.as_view(), name="positions"),
    path("tasktype", TaskTypeListView.as_view(), name="task-type"),
    path("task/<int:pk>/toggle/", toggle_assign_to_task, name="toggle-task"),
    path("accounts/login/", login_view, name="login"),
]


app_name = "manager"
