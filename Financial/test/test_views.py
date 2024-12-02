from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from Financial.models import FinancialRecord
from Projects.models import Project
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class FinancialRecordViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number="09351281828",
            first_name="Test",
            last_name="User",
            role="CEO",
            email="test@example.com",
            password="Password@1234",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.project = Project.objects.create(
            title="Test Project",
            user=self.user,
            description="Test project description",
            color="blue",
        )

        self.financial_url = reverse("financial:list_create_financial_record")

    def test_list_financial_records(self):
        """
        Test listing financial records for the authenticated user.
        """
        FinancialRecord.objects.create(
            who_created=self.user,
            title="Test Financial Record",
            price=1500.00,
            description="Test financial description",
            status="paid",
            content_type=ContentType.objects.get_for_model(self.project),
            object_id=self.project.id,
        )

        response = self.client.get(self.financial_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
 
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Financial Record")

    def test_create_financial_record(self):
        """
        Test creating a new financial record.
        """
        data = {
            "title": "New Financial Record",
            "price": 2500.00,
            "description": "Test description",
            "status": "paid",
            "content_type": ContentType.objects.get_for_model(self.project).id,
            "object_id": self.project.id,
        }

        response = self.client.post(self.financial_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FinancialRecord.objects.count(), 1)
        self.assertEqual(FinancialRecord.objects.first().title, "New Financial Record")

    def test_unauthenticated_access(self):
        """
        Test that unauthenticated users cannot access the endpoint.
        """
        self.client.logout()
        response = self.client.get(self.financial_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
