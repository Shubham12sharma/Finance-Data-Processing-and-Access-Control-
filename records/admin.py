from django.contrib import admin
from .models import FinancialRecord


@admin.register(FinancialRecord)
class FinancialRecordAdmin(admin.ModelAdmin):
    """Admin interface for Financial Records with filtering and search"""
    list_display = ('id', 'user', 'record_type', 'amount', 'category', 'date', 'is_deleted', 'created_at')
    list_filter = ('record_type', 'category', 'date', 'is_deleted', 'user')
    search_fields = ('user__username', 'user__email', 'description', 'category')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Transaction Info', {'fields': ('user', 'record_type', 'amount', 'category')}),
        ('Details', {'fields': ('date', 'description')}),
        ('Status', {'fields': ('is_deleted',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    
    def get_queryset(self, request):
        """Show all records to superusers (including soft-deleted ones)"""
        qs = super().get_queryset(request)
        return qs
