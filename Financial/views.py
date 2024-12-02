from .models import FinancialRecord
from .serializers import FinancialRecordSerializers
from rest_framework import generics
from .filters import ListOfFinancialPerformanceFilterBackend


class FinancialListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating financial records.

    This endpoint allows authenticated users to:
    - **List financial records** they have created, sorted by price in descending order.
    - **Create a new financial record** and associate it with their user account.

    - **Method:** GET, POST  
    - **Request Body (POST):** Includes financial record details such as title, price, description, status, and related object (project, task, or subtask).  
    - **Permissions:** Requires user authentication.  
    - **Response:**
        - **GET:** Returns a paginated list of financial records created by the authenticated user.
        - **POST:** Returns the created financial record.

    **Filters:**  
    Supports filtering financial records using the `ListOfFinancialPerformanceFilterBackend`.
    """
    serializer_class = FinancialRecordSerializers
    filter_backends = [ListOfFinancialPerformanceFilterBackend]

    def get_queryset(self):
        user = self.request.user
        return FinancialRecord.objects.filter(who_created=user).order_by('-price')

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(who_created=self.request.user)
