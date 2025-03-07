from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from manager.models import Task, Position, Project, Team, TaskType

User = get_user_model()


class ViewsTestCase(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.user = User.objects.create_user(username="testuser", password="testpass", position=self.position)
        self.client.login(username="testuser", password="testpass")

        self.team = Team.objects.create(name="Test Team")
        self.team.members.add(self.user)

        self.project = Project.objects.create(name="Test Project", description="Project Description", team=self.team)
        self.task_type = TaskType.objects.create(name="Bug Fix")
        self.task = Task.objects.create(name="Test Task", description="Task Description", project=self.project,
                                        task_type=self.task_type)
        self.task.assignees.add(self.user)

    def test_index_view(self):
        response = self.client.get(reverse("manager:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/index.html")

    def test_task_detail_view(self):
        response = self.client.get(reverse("manager:task-detail", args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_toggle_assign_to_task(self):
        response = self.client.post(reverse("manager:toggle-task", args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertNotIn(self.user, self.task.assignees.all())

        response = self.client.post(reverse("manager:toggle-task", args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertIn(self.user, self.task.assignees.all())

    def test_worker_list_view(self):
        response = self.client.get(reverse("manager:workers"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_project_list_view(self):
        response = self.client.get(reverse("manager:projects"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.name)

    def test_project_create_view(self):
        response = self.client.post(reverse("manager:project-create"), {
            "name": "New Project",
            "description": "New Description",
            "deadline": "2025-12-31",
            "is_completed": False,
            "team": self.team.pk
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Project.objects.filter(name="New Project").exists())
