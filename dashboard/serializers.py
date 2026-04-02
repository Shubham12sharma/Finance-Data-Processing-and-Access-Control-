from rest_framework import serializers

class DashboardSummarySerializer(serializers.Serializer):
    """Serializer for dashboard summary data"""
    total_income = serializers.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_balance = serializers.DecimalField(max_digits=12, decimal_places=2, default=0)
    category_breakdown = serializers.DictField(default=dict)
    recent_activity = serializers.ListField(default=list)
    total_records = serializers.IntegerField(default=0)