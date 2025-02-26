from django.contrib.admin.sites import site
from django.test import TestCase
from django.contrib.auth import get_user_model
from manager.models import Worker, Position, TaskType, Task, Team, Project
from manager.admin import WorkerAdmin, TaskAdmin, ProjectAdmin


class AdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.position = Position.objects.create(name="Manager")
        cls.worker = get_user_model().objects.create_user(
            username="testuser",
            password="password123",
            first_name="John",
            last_name="Doe",
            position=cls.position,
        )

    def test_worker_registered_in_admin(self):
        self.assertIn(Worker, site._registry)

    def test_worker_admin_list_display(self):
        admin_instance = WorkerAdmin(model=Worker, admin_site=site)
        self.assertIn("position", admin_instance.list_display)

    def test_worker_admin_list_filter(self):
        admin_instance = WorkerAdmin(model=Worker, admin_site=site)
        self.assertIn("position", admin_instance.list_filter)

    def test_worker_admin_fieldsets(self):
        admin_instance = WorkerAdmin(model=Worker, admin_site=site)
        fieldset_names = [fieldset[0] for fieldset in admin_instance.fieldsets]
        self.assertIn("Additional info", fieldset_names)

    def test_task_registered_in_admin(self):
        self.assertIn(Task, site._registry)

    def test_task_admin_list_display(self):
        admin_instance = TaskAdmin(model=Task, admin_site=site)
        expected_fields = ("name", "deadline", "priority", "task_type", "project")
        self.assertEqual(admin_instance.list_display, expected_fields)

    def test_task_admin_list_filter(self):
        admin_instance = TaskAdmin(model=Task, admin_site=site)
        self.assertIn("task_type", admin_instance.list_filter)

    def test_project_registered_in_admin(self):
        self.assertIn(Project, site._registry)

    def test_project_admin_list_display(self):
        admin_instance = ProjectAdmin(model=Project, admin_site=site)
        expected_fields = ("name", "team")
        self.assertEqual(admin_instance.list_display, expected_fields)

    def test_models_registered_in_admin(self):
        for model in [Position, TaskType, Team]:
            with self.subTest(model=model):
                self.assertIn(model, site._registry)
