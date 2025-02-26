from django.test import TestCase
from manager.forms import (
    WorkerCreationForm, WorkerUpdateForm, TaskForm,
    WorkerSearchForm, ProjectSearchForm, TeamSearchForm, TeamForm
)
from manager.models import Worker, Position, Task, Project, Team, TaskType
import datetime

class FormsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.position = Position.objects.create(name="Manager")
        cls.worker = Worker.objects.create_user(
            username="testuser",
            password="password123",
            first_name="John",
            last_name="Doe",
            position=cls.position,
        )
        cls.team = Team.objects.create(name="Development")
        cls.team.members.add(cls.worker)
        cls.project = Project.objects.create(name="Test Project", team=cls.team)
        cls.task_type = TaskType.objects.create(name="Bugfix")
        cls.task = Task.objects.create(
            name="Sample Task",
            description="Task Description",
            deadline=datetime.date.today() + datetime.timedelta(days=5),
            is_completed=False,
            priority=2,
            task_type=cls.task_type,
            project=cls.project,
        )

    def test_worker_creation_form_valid(self):
        form = WorkerCreationForm(data={
            "username": "newuser",
            "password1": "SecurePass123",
            "password2": "SecurePass123",
            "first_name": "Jane",
            "last_name": "Doe",
            "position": self.position.id
        })
        self.assertTrue(form.is_valid())

    def test_worker_update_form_valid(self):
        form = WorkerUpdateForm(instance=self.worker, data={
            "username": "updated_user",
            "first_name": "Updated",
            "last_name": "User",
            "position": self.position.id,
            "email": "user@example.com"
        })
        self.assertTrue(form.is_valid())

    def test_task_form_valid(self):
        form = TaskForm(data={
            "name": "New Task",
            "description": "Some task",
            "deadline": datetime.date.today() + datetime.timedelta(days=2),
            "is_completed": False,
            "priority": 2,
            "task_type": self.task_type.id,
            "assignees": [self.worker.id]
        }, project=self.project)
        self.assertTrue(form.is_valid())

    def test_task_form_invalid_deadline(self):
        form = TaskForm(data={
            "name": "Invalid Task",
            "description": "Should fail",
            "deadline": datetime.date.today() - datetime.timedelta(days=1),  # минула дата
            "is_completed": False,
            "priority": 2,
            "task_type": "Bugfix",
            "assignees": [self.worker.id]
        }, project=self.project)
        self.assertFalse(form.is_valid())
        self.assertIn("deadline", form.errors)

    def test_search_forms(self):
        worker_search = WorkerSearchForm(data={"username": "testuser"})
        project_search = ProjectSearchForm(data={"name": "Test Project"})
        team_search = TeamSearchForm(data={"name": "Development"})
        self.assertTrue(worker_search.is_valid())
        self.assertTrue(project_search.is_valid())
        self.assertTrue(team_search.is_valid())

    def test_team_form_valid(self):
        form = TeamForm(data={"name": "QA Team", "members": [self.worker.id]})
        self.assertTrue(form.is_valid())
