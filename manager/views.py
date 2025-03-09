from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from manager.forms import (
    WorkerCreationForm,
    WorkerUpdateForm,
    TaskForm,
    WorkerSearchForm,
    ProjectSearchForm,
    TeamForm,
    TeamSearchForm,
    LoginForm,
)
from manager.models import Task, Worker, Position, TaskType, Project, Team


@login_required
def index(request):
    num_task = Task.objects.count()
    num_worker = Worker.objects.count()
    num_free_workers = (
        Worker.objects.annotate(task_count=Count("workers"))
        .filter(task_count=0)
        .count()
    )
    num_project = Project.objects.count()
    num_teams = Team.objects.count()
    context = {
        "num_task": num_task,
        "num_worker": num_worker,
        "num_free_workers": num_free_workers,
        "num_project": num_project,
        "num_teams": num_teams,
    }
    return render(request, "manager/index.html", context)


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = "Invalid credentials"
        else:
            msg = "Error validating the form"

    return render(request, "registration/login.html", {"form": form, "msg": msg})


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        project = get_object_or_404(Project, pk=self.kwargs.get("project_id"))
        kwargs["project"] = project
        return kwargs

    def form_valid(self, form):
        form.instance.project = get_object_or_404(
            Project, pk=self.kwargs.get("project_id")
        )
        return super().form_valid(form)


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
    paginate_by = 5

    def get_queryset(self):
        queryset = Worker.objects.select_related("position")
        username = self.request.GET.get("username")
        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerSearchForm(initial={"username": username})
        return context


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


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project

    def get_queryset(self):
        queryset = Project.objects.all()
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = ProjectSearchForm(initial={"name": name})
        return context


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = self.object.task_set.all()
        return context


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    fields = "__all__"


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    fields = "__all__"


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("manager:projects")


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team

    def get_queryset(self):
        queryset = Team.objects.all()
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TeamSearchForm(initial={"name": name})
        return context


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects"] = self.object.project_set.all()
        return context


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamForm


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamForm


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("manager:teams")


@login_required
def toggle_assign_to_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    if request.user in task.assignees.all():
        task.assignees.remove(request.user)
    else:
        task.assignees.add(request.user)
    return HttpResponseRedirect(reverse_lazy("manager:task-detail", args=[pk]))
