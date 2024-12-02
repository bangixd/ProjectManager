from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from Projects.models import Project, Task, SubTask
from django.contrib.auth import get_user_model


class ProjectViewsTest(APITestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            phone_number="09351281828",
            first_name="U_1",
            last_name="F_1",
            role="CEO",
            email="test@gmail.com",
            password="Password@1234"
        )
        self.user = user
        self.client.login(phone_number="09351281828", password="Password@1234")
        self.project = Project.objects.create(
            title="Test Project",
            user=user,
            description="Test description",
            color="blue",
            start_date="2024-01-01",
            end_date="2024-12-31",
            status=True
        )
        self.project_url = reverse('projects:project_list_create')

    def test_project_list_create(self):
        """
        Test listing and creating projects.
        """
        response = self.client.post(self.project_url, {
            'title': 'New Project',
            'user': self.user.id,
            'description': 'New project description',
            'color': 'red',
            'start_date': '2024-01-01',
            'end_date': '2024-12-31',
            'status': True,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(self.project_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)


class TaskViewsTest(APITestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            phone_number="09351281828",
            first_name="U_1",
            last_name="F_1",
            role="CEO",
            email="test@gmail.com",
            password="Password@1234"
        )
        self.user = user
        self.client.login(phone_number="09351281828", password="Password@1234")
        self.project = Project.objects.create(
            title="Test Project",
            user=user,
            description="Test description",
            color="blue",
            start_date="2024-01-01",
            end_date="2024-12-31",
            status=True
        )
        self.task_url = reverse('projects:create_list_task_project', kwargs={'pk': self.project.id})

    def test_task_list_create(self):
        """
        Test listing and creating tasks.
        """
        response = self.client.post(self.task_url, {
            'title': 'Test Task',
            'description': 'Test task description',
            'color': 'green',
            'start_date': '2024-01-01',
            'end_date': '2024-06-30',
            'status': True,
            'project': self.project.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # List tasks
        response = self.client.get(self.task_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)


class SubtaskViewsTest(APITestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            phone_number="09351281828",
            first_name="F_1",
            last_name="L_1",
            role="CEO",
            email="test@gmail.com",
            password="Password@1234"
        )
        self.user = user
        self.client.login(phone_number="09351281828", password="Password@1234")
        self.project = Project.objects.create(
            title="Test Project",
            user=user,
            description="Test description",
            color="blue",
            start_date="2024-01-01",
            end_date="2024-12-31",
            status=True
        )
        self.task = Task.objects.create(
            project=self.project,
            title="Test Task",
            description="Test task description",
            color="green",
            start_date="2024-01-01",
            end_date="2024-06-30",
            status=True
        )
        self.subtask_url = reverse('projects:create_list_subtask_project', kwargs={'pk': self.task.id})

    def test_subtask_list_create(self):
        """
        Test listing and creating subtasks.
        """
        response = self.client.post(self.subtask_url, {
            'title': 'Test Subtask',
            'description': 'Test subtask description',
            'color': 'yellow',
            'start_date': '2024-01-01',
            'end_date': '2024-03-31',
            'status': True,
            'task': self.task.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

       
