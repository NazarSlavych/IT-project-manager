import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm

from manager.models import Worker, Task, Team


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position",
        )


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ("username", "first_name", "last_name", "position", "email")


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "deadline", "is_completed","priority", "task_type", "assignees"]
        widgets = {
            "assignees": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        project = kwargs.pop("project", None)
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            project = self.instance.project

        if project:
            self.fields["assignees"].queryset = project.team.members.all()

    def clean_deadline(self):
        deadline = self.cleaned_data["deadline"]
        if deadline < datetime.date.today():
            raise forms.ValidationError("Deadline must be in the future")
        return deadline


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username.."})
    )

class ProjectSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name.."})
    )

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = "__all__"
        widgets = {
            "members": forms.CheckboxSelectMultiple(),
        }
