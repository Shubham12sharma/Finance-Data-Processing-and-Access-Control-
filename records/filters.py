import django_filters
from .models import FinancialRecord

class FinancialRecordFilter(django_filters.FilterSet):
    """Advanced filtering for financial records"""
    start_date = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    min_amount = django_filters.NumberFilter(field_name='amount', lookup_expr='gte')
    max_amount = django_filters.NumberFilter(field_name='amount', lookup_expr='lte')

    class Meta:
        model = FinancialRecord
        fields = {
            'record_type': ['exact'],
            'category': ['exact'],
            'date': ['exact'],
        }