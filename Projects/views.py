from .models import Project, Task, SubTask
from rest_framework import generics, permissions
from .serializers import ProjectSerializers, TaskSerializer, SubtaskSerializers
from .paginations import ProjectTaskSubtaskPagination
from .permissions import CanUpdateDestroyProject, CanUpdateDestroyTask, CanUpdateDestroySubtask
from django.shortcuts import get_object_or_404
from rest_framework import serializers

class ProjectListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating projects.

    - **Method:** GET, POST  
    - **Request Body (POST):** Project details (title, description, color, image, etc.)
    - **Permissions:** Requires user authentication.  
    - **Response:** Returns a list of projects for GET requests and the created project for POST requests.
    """
    
    serializer_class = ProjectSerializers
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ProjectTaskSubtaskPagination
    
    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)

class ProjectListUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, or deleting a specific project.

    - **Method:** GET, PUT, DELETE  
    - **Request Body (PUT):** Project details (fields to be updated).  
    - **Permissions:** Requires user authentication and ownership of the project.  
    - **Response:** Returns the project details for GET requests, updated details for PUT, and a success message for DELETE.
    """
    
    serializer_class = ProjectSerializers
    permission_classes = [permissions.IsAuthenticated, CanUpdateDestroyProject]
    queryset = Project
    lookup_field = 'pk'

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

class TaskProjectListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing tasks of a project or creating a new task under a specific project.

    - **Method:** GET, POST  
    - **Request Body (POST):** Task details (title, description, color, image, etc.).  
    - **Permissions:** Requires user authentication.  
    - **Response:** Returns a list of tasks for GET requests or the created task for POST requests.
    """
    
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    lookup_field = 'pk'
    pagination_class = ProjectTaskSubtaskPagination

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Project.objects.none()

        tasks = Task.objects.filter(project_id=self.kwargs['pk'])
        return tasks

    def perform_create(self, serializer):
        pj = get_object_or_404(Project, id=self.kwargs['pk'])
        if serializer.is_valid():
            serializer.save(project=pj)
    
class TaskListUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, or deleting a specific task.

    - **Method:** GET, PUT, DELETE  
    - **Request Body (PUT):** Task details (fields to be updated).  
    - **Permissions:** Requires user authentication and ownership of the associated project.  
    - **Response:** Returns task details for GET, updated details for PUT, and a success message for DELETE.
    """
    
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, CanUpdateDestroyTask]
    queryset = Task
    lookup_field = 'pk'

    def perform_update(self, serializer):
        if serializer.is_valid():
            if getattr(self, 'swagger_fake_view', False):
                return Task.objects.none()
            
            # Safely retrieve task object
            try:
                task_id = self.kwargs.get('pk')  # Ensure pk is valid
                task = Task.objects.get(id=task_id)
            except (Task.DoesNotExist, ValueError):
                raise serializers.ValidationError("Invalid task ID provided.")
            
            image = serializer.validated_data.get('image', None)
            if image is None:
                serializer.save(image=task.image)  # Preserve existing image if not provided
            else:
                serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

class SubtaskListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing subtasks of a task or creating a new subtask under a specific task.

    - **Method:** GET, POST  
    - **Request Body (POST):** Subtask details (title, description, color, image, etc.).  
    - **Permissions:** Requires user authentication.  
    - **Response:** Returns a list of subtasks for GET requests or the created subtask for POST requests.
    """
    serializer_class = SubtaskSerializers
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'
    pagination_class = ProjectTaskSubtaskPagination

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return SubTask.objects.none()

        task = get_object_or_404(Task, id=self.kwargs['pk'])
        return SubTask.objects.filter(task=task)

    def perform_create(self, serializer):
        task = get_object_or_404(Task, id=self.kwargs['pk'])
        if serializer.is_valid():
            serializer.save(task=task)

class SubtaskUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, or deleting a specific subtask.

    - **Method:** GET, PUT, DELETE  
    - **Request Body (PUT):** Subtask details (fields to be updated).  
    - **Permissions:** Requires user authentication and ownership of the associated project.  
    - **Response:** Returns subtask details for GET, updated details for PUT, and a success message for DELETE.
    """
    
    serializer_class = SubtaskSerializers
    permission_classes = [permissions.IsAuthenticated, CanUpdateDestroySubtask]
    queryset = SubTask
    lookup_field = 'pk'
    
    def perform_update(self, serializer):
        image = serializer.validated_data.get('image')
        if image is None:
            subtask = self.get_object()  
            serializer.save(image=subtask.image)
        else:
            serializer.save()
    
    def perform_destroy(self, instance):
        instance.delete()
