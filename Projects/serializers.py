from rest_framework import serializers
from .models import Project, Task, SubTask

class ProjectSerializers(serializers.ModelSerializer):
    """
        Serializer for the Project model.

        - **Fields:**
            - `pk`: Primary key of the project.
            - `title`: Title of the project.
            - `user`: User associated with the project (read-only).
            - `description`: Description of the project.
            - `color`: Color of the project (e.g., 'red', 'blue').
            - `image`: Image associated with the project.
            - `start_date`: Start date of the project.
            - `end_date`: End date of the project.
            - `status`: Current status of the project (boolean).
            - `budget`: Budget allocated for the project.

        - **Extra Configurations:**
            - The `user` field is read-only and automatically assigned.
    """
    
    class Meta:
        model = Project
        fields = [
            'pk',
            'title',
            'user',
            'description',
            'color',
            'image',
            'start_date',
            'end_date',
            'status',
            'budget',
            'content_id',
        ]
        extra_kwargs = {
            'user': {'read_only': True}
        }

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.

    - **Fields:**
        - `pk`: Primary key of the task.
        - `project`: Project the task belongs to (read-only).
        - `title`: Title of the task.
        - `image`: Image associated with the task.
        - `color`: Color of the task (e.g., 'red', 'green').
        - `description`: Description of the task.
        - `budget`: Budget allocated for the task.
        - `start_date`: Start date of the task.
        - `end_date`: End date of the task.
        - `status`: Current status of the task (boolean).

    - **Depth:**
        - Includes details of the related project (`depth=1`).
    - **Extra Configurations:**
        - The `project` field is read-only and assigned automatically.
    """

    class Meta:
        model = Task
        fields = [
            'pk',
            'project',
            'title',
            'image',
            'color',
            'description',
            'budget',
            'start_date',
            'end_date',
            'status',
            'content_id',
        ]
        depth = 1
        extra_kwargs = {
            'project': {'read_only': True},
        }

class SubtaskSerializers(serializers.ModelSerializer):
    """
    Serializer for the SubTask model.

    - **Fields:**
        - `pk`: Primary key of the subtask.
        - `task`: Task the subtask belongs to (read-only).
        - `title`: Title of the subtask.
        - `image`: Image associated with the subtask.
        - `color`: Color of the subtask (e.g., 'yellow', 'blue').
        - `description`: Description of the subtask.
        - `budget`: Budget allocated for the subtask.
        - `start_date`: Start date of the subtask.
        - `end_date`: End date of the subtask.
        - `status`: Current status of the subtask (boolean).

    - **Depth:**
        - Includes details of the related task and project (`depth=2`).
    - **Extra Configurations:**
        - The `task` field is read-only and assigned automatically.
    """
    
    class Meta:
        model = SubTask
        fields = [
            'pk',
            'task',
            'title',
            'image',
            'color',
            'description',
            'budget',
            'start_date',
            'end_date',
            'status',
            'content_id',
        ]
        depth = 2
        extra_kwargs = {
            'task': {'read_only': True},
        }
