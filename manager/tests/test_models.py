import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from manager.models import Position, TaskType, Team, Project, Task


class PositionModelTest(TestCase):
    def test_create_position(self):
        position = Position.objects.create(name="Developer")
        self.assertEqual(str(position), "Developer")


class WorkerModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Manager")
        self.worker = get_user_model().objects.create_user(
            username="testuser",
            password="password123",
            first_name="John",
            last_name="Doe",
            position=self.position,
        )

    def test_create_worker(self):
        self.assertEqual(self.worker.username, "testuser")
        self.assertEqual(self.worker.position.name, "Manager")
        self.assertTrue(self.worker.check_password("password123"))

    def test_worker_str(self):
        self.assertEqual(
            str(self.worker),
            f"{self.worker.username}: ({self.worker.first_name} {self.worker.last_name})",
        )


class TaskTypeModelTest(TestCase):
    def test_create_task_type(self):
        task_type = TaskType.objects.create(name="Bug Fix")
        self.assertEqual(str(task_type), "Bug Fix")


class TeamModelTest(TestCase):
    def setUp(self):
        self.worker1 = get_user_model().objects.create_user(
            username="worker1", password="testpass"
        )
        self.worker2 = get_user_model().objects.create_user(
            username="worker2", password="testpass"
        )

    def test_create_team(self):
        team = Team.objects.create(name="Development Team")
        team.members.set([self.worker1, self.worker2])
        self.assertEqual(str(team), "Development Team")
        self.assertEqual(team.members.count(), 2)

    def test_team_str(self):
        team = Team.objects.create(name="Development Team")
        self.assertEqual(str(team), "Development Team")


class ProjectModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="Design Team")
        self.project = Project.objects.create(
            name="Website Redesign",
            description="Redesign the company website",
            deadline=datetime.date.today(),
            team=self.team,
        )

    def test_create_project(self):
        self.assertEqual(str(self.project.name), "Website Redesign")
        self.assertEqual(self.project.team.name, "Design Team")

    def test_project_str(self):
        self.assertEqual(str(self.project), "Website Redesign")


class TaskModelTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Feature")
        self.team = Team.objects.create(name="Frontend Team")
        self.project = Project.objects.create(
            name="Landing Page",
            description="Create a landing page",
            deadline=datetime.date.today(),
            team=self.team,
        )
        self.worker1 = get_user_model().objects.create_user(
            username="worker1", password="testpass"
        )
        self.worker2 = get_user_model().objects.create_user(
            username="worker2", password="testpass"
        )

    def test_create_task(self):
        task = Task.objects.create(
            name="Create Navbar",
            description="Implement a responsive navbar",
            deadline=datetime.date.today(),
            is_completed=False,
            priority=1,
            task_type=self.task_type,
            project=self.project,
        )
        task.assignees.set([self.worker1, self.worker2])

        self.assertEqual(str(task), "Create Navbar")
        self.assertEqual(task.task_type.name, "Feature")
        self.assertEqual(task.project.name, "Landing Page")
        self.assertEqual(task.assignees.count(), 2)
