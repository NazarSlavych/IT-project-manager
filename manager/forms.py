import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm

from manager.models import Worker, Task


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
        fields = "__all__"
        widgets = {
            "assignees": forms.CheckboxSelectMultiple(),
        }

    def clean_deadline(self):
        deadline = self.cleaned_data["deadline"]
        if deadline < datetime.date.today():
            raise forms.ValidationError("Deadline must be in the future")
        return deadline


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name.."})
    )


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username.."})
    )