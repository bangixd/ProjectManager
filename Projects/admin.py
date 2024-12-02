from django.contrib import admin
from .models import Project, Task, SubTask


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'color', 'budget', 'start_date', 'end_date')
    list_filter = ('color', 'status', 'start_date', 'end_date')
    search_fields = ('title', 'description', 'user__username')
    actions = ['mark_as_completed', 'reset_budget']

    def mark_as_completed(self, request, queryset):
        queryset.update(status=True)
        self.message_user(request, "Selected projects have been marked as completed.")
    mark_as_completed.short_description = "Mark selected projects as completed"

    def reset_budget(self, request, queryset):
        queryset.update(budget=0)
        self.message_user(request, "Budget reset for selected projects.")
    reset_budget.short_description = "Reset budget for selected projects"



@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'color', 'budget', 'start_date', 'end_date')
    list_filter = ('color', 'status', 'start_date', 'end_date', 'project__user')
    search_fields = ('title', 'description', 'project__title')
    actions = ['mark_as_completed', 'duplicate_tasks']

    def mark_as_completed(self, request, queryset):
        queryset.update(status=True)
        self.message_user(request, "Selected tasks have been marked as completed.")
    mark_as_completed.short_description = "Mark selected tasks as completed"

    def duplicate_tasks(self, request, queryset):
        for task in queryset:
            task.pk = None
            task.title += " (Copy)"
            task.save()
        self.message_user(request, "Selected tasks have been duplicated.")
    duplicate_tasks.short_description = "Duplicate selected tasks"


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'color', 'budget', 'start_date', 'end_date')
    list_filter = ('color', 'status', 'start_date', 'end_date', 'task__project')
    search_fields = ('title', 'description', 'task__title', 'task__project__title')
    actions = ['mark_as_completed', 'assign_color']

    def mark_as_completed(self, request, queryset):
        queryset.update(status=True)
        self.message_user(request, "Selected subtasks have been marked as completed.")
    mark_as_completed.short_description = "Mark selected subtasks as completed"

    def assign_color(self, request, queryset):
        queryset.update(color='yellow')
        self.message_user(request, "Color 'yellow' assigned to selected subtasks.")
    assign_color.short_description = "Assign 'yellow' color to selected subtasks"
