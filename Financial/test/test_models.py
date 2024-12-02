from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from Financial.models import FinancialRecord
from Projects.models import Project

User = get_user_model()

class FinancialRecordModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number="09351281828",
            first_name="Test",
            last_name="User",
            role="CEO",
            email="test@example.com",
            password="Password@1234",
        )

        self.project = Project.objects.create(
            title="Test Project",
            user=self.user,
            description="Test project description",
            color="blue",
        )

        self.financial_record = FinancialRecord.objects.create(
            who_created=self.user,
            title="Test Financial Record",
            price=1500.00,
            description="Test financial description",
            status="paid",
            content_type=ContentType.objects.get_for_model(self.project),
            object_id=self.project.id,
        )

    def test_financial_record_creation(self):
        """
        Test that a financial record is created successfully.
        """
        self.assertEqual(FinancialRecord.objects.count(), 1)
        self.assertEqual(self.financial_record.title, "Test Financial Record")
        self.assertEqual(self.financial_record.price, 1500.00)
        self.assertEqual(self.financial_record.status, "paid")

    def test_financial_record_kind_property(self):
        """
        Test the 'kind' property returns the correct object type.
        """
        self.assertEqual(self.financial_record.kind, "project")

    def test_financial_record_relationship(self):
        """
        Test the relationship between FinancialRecord and the related object.
        """
        self.assertEqual(self.financial_record.content_object, self.project)
