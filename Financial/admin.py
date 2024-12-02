from django.contrib import admin
from .models import FinancialRecord

@admin.register(FinancialRecord)
class FinancialRecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'status', 'create', 'update', 'kind', 'who_created')
    list_filter = ('status', 'create', 'update', 'content_type')
    search_fields = ('title', 'description', 'who_created__username', 'content_type__model')
    actions = ['mark_as_paid', 'filter_by_project']

    def mark_as_paid(self, request, queryset):
        queryset.update(status='paid')
        self.message_user(request, "Selected financial records have been marked as paid.")
    mark_as_paid.short_description = "Mark selected records as paid"

    def filter_by_project(self, request, queryset):
        filtered = queryset.filter(content_type__model='project')
        self.message_user(request, f"{filtered.count()} records related to projects have been filtered.")
    filter_by_project.short_description = "Filter records related to projects"

    def kind(self, obj):
        return obj.kind
    kind.short_description = "Related Type (Project/Task/SubTask)"