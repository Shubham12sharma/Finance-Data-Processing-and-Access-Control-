from django.db.models import Sum, Q
from .models import FinancialRecord

def get_user_records(user, filters=None):
    """Get records for a specific user with soft delete filter"""
    queryset = FinancialRecord.objects.filter(user=user, is_deleted=False)
    
    if filters:
        queryset = queryset.filter(**filters)
    
    return queryset


def calculate_record_stats(records):
    """Calculate basic stats for a queryset of records"""
    income = records.filter(record_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    expenses = records.filter(record_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    
    return {
        'total_income': float(income),
        'total_expenses': float(expenses),
        'net_balance': float(income - expenses),
    }