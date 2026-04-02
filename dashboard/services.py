from django.db.models import Sum, Q, Count
from records.models import FinancialRecord
from datetime import datetime, timedelta

def get_dashboard_summary(user):
    """
    Generate comprehensive dashboard summary for a user.
    This service layer keeps the logic clean and reusable.
    """
    # Get only user's non-deleted records
    records = FinancialRecord.objects.filter(user=user, is_deleted=False)

    # Basic totals
    totals = records.aggregate(
        total_income=Sum('amount', filter=Q(record_type='income')),
        total_expenses=Sum('amount', filter=Q(record_type='expense')),
        total_records=Count('id')
    )

    total_income = totals['total_income'] or 0
    total_expenses = totals['total_expenses'] or 0
    net_balance = total_income - total_expenses

    # Category-wise breakdown
    category_breakdown = {}
    category_data = records.values('category').annotate(
        total=Sum('amount')
    ).order_by('-total')

    for item in category_data:
        if item['total']:
            category_breakdown[item['category']] = float(item['total'])

    # Recent activity (last 5 records)
    recent_records = records.order_by('-date', '-created_at')[:5]
    recent_activity = [
        {
            'id': record.id,
            'amount': float(record.amount),
            'record_type': record.record_type,
            'category': record.category,
            'date': record.date.strftime('%Y-%m-%d'),
            'description': record.description
        }
        for record in recent_records
    ]

    # Monthly trend (simple last 3 months)
    current_month = datetime.now().replace(day=1)
    monthly_trend = []
    
    for i in range(3):
        month_start = current_month - timedelta(days=30*i)
        month_end = month_start + timedelta(days=30)
        
        month_data = records.filter(
            date__gte=month_start.date(),
            date__lt=month_end.date()
        ).aggregate(
            income=Sum('amount', filter=Q(record_type='income')),
            expenses=Sum('amount', filter=Q(record_type='expense'))
        )
        
        monthly_trend.append({
            'month': month_start.strftime('%b %Y'),
            'income': float(month_data['income'] or 0),
            'expenses': float(month_data['expenses'] or 0)
        })

    return {
        'total_income': float(total_income),
        'total_expenses': float(total_expenses),
        'net_balance': float(net_balance),
        'category_breakdown': category_breakdown,
        'recent_activity': recent_activity,
        'total_records': totals['total_records'] or 0,
        'monthly_trend': monthly_trend
    }