from django.test import TestCase
from Projects.models import Project, Task, SubTask
from django.contrib.auth import get_user_model

class ProjectModelTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            phone_number="09351281828",
            first_name="F_1",
            last_name="L_1",
            role="CEO",
            email="test@gmail.com",
            password="Password@1234"
        )
        self.project = Project.objects.create(
            title="Test Project",
            user=user,
            description="Test description",
            color="blue",
            start_date="2024-01-01",
            end_date="2024-12-31",
            status=True,
        )

    def test_project_creation(self):
        project = self.project
        self.assertEqual(project.title, "Test Project")
        self.assertEqual(project.user.phone_number, "09351281828")
        self.assertEqual(project.color, "blue")
        self.assertTrue(project.status)

    def test_project_str(self):
        project = self.project
        self.assertEqual(str(project), "Test Project")

class TaskModelTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            phone_number="09351281828",
            first_name="U_1",
            last_name="F_1",
            role="CEO",
            email="test@gmail.com",
            password="Password@1234"
        )
        project = Project.objects.create(
            title="Test Project",
            user=user,
            description="Test description",
            color="blue",
            start_date="2024-01-01",
            end_date="2024-12-31",
            status=True,
        )
        self.task = Task.objects.create(
            project=project,
            title="Test Task",
            description="Test task description",
            color="red",
            start_date="2024-01-01",
            end_date="2024-06-30",
            status=True
        )

    def test_task_creation(self):
        task = self.task
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.project.title, "Test Project")
        self.assertEqual(task.color, "red")
        self.assertTrue(task.status)

    def test_task_str(self):
        task = self.task
        self.assertEqual(str(task), "Test Task")


class SubTaskModelTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            phone_number="09351281828",
            first_name="F_1",
            last_name="L_1",
            role="CEO",
            email="test@gmail.com",
            password="Password@1234"
        )
        project = Project.objects.create(
            title="Test Project",
            user=user,
            description="Test description",
            color="blue",
            start_date="2024-01-01",
            end_date="2024-12-31",
            status=True,
        )
        task = Task.objects.create(
            project=project,
            title="Test Task",
            description="Test task description",
            color="red",
            start_date="2024-01-01",
            end_date="2024-06-30",
            status=True
        )
        self.subtask = SubTask.objects.create(
            task=task,
            title="Test Subtask",
            description="Test subtask description",
            color="green",
            start_date="2024-01-01",
            end_date="2024-03-31",
            status=True
        )

    def test_subtask_creation(self):
        subtask = self.subtask
        self.assertEqual(subtask.title, "Test Subtask")
        self.assertEqual(subtask.task.title, "Test Task")
        self.assertEqual(subtask.color, "green")
        self.assertTrue(subtask.status)

    def test_subtask_str(self):
        subtask = self.subtask
        self.assertEqual(str(subtask), "Test Subtask")