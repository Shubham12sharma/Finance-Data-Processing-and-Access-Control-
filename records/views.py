from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from common.permissions import IsAdmin, IsAnalystOrHigher, IsViewerOrHigher, IsOwner
from .models import FinancialRecord
from .serializers import FinancialRecordSerializer
from .filters import FinancialRecordFilter
from .services import get_user_records

class FinancialRecordViewSet(viewsets.ModelViewSet):
    serializer_class = FinancialRecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FinancialRecordFilter

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Only Analyst and Admin can modify records
            return [IsAnalystOrHigher()]
        # Viewer, Analyst, Admin can read
        return [IsViewerOrHigher()]

    def get_queryset(self):
        """Users can only see their own records"""
        return get_user_records(self.request.user)

    def perform_create(self, serializer):
        """Automatically assign record to current user"""
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        """Soft delete instead of hard delete"""
        instance.soft_delete()

    # Optional: Get basic stats for current user's records
    @action(detail=False, methods=['get'])
    def stats(self, request):
        records = self.get_queryset()
        from .services import calculate_record_stats
        stats = calculate_record_stats(records)
        return Response(stats)