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
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'bulk_delete', 'restore']:
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

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get statistics for current user's records"""
        records = self.get_queryset()
        from .services import calculate_record_stats
        stats = calculate_record_stats(records)
        return Response(stats)
    
    @action(detail=False, methods=['post'])
    def bulk_delete(self, request):
        """Delete multiple records at once"""
        ids = request.data.get('ids', [])
        if not ids:
            return Response(
                {'error': 'No record IDs provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        records = self.get_queryset().filter(id__in=ids)
        deleted_count = 0
        for record in records:
            record.soft_delete()
            deleted_count += 1
        
        return Response({
            'deleted_count': deleted_count,
            'message': f'{deleted_count} records deleted successfully'
        })
    
    @action(detail=False, methods=['get'])
    def deleted(self, request):
        """Get all soft-deleted records for current user"""
        deleted_records = FinancialRecord.objects.filter(
            user=request.user,
            is_deleted=True
        )
        serializer = self.get_serializer(deleted_records, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """Restore a soft-deleted record"""
        record = self.get_object()
        if record.is_deleted:
            record.is_deleted = False
            record.save()
            return Response({
                'message': 'Record restored successfully',
                'record': FinancialRecordSerializer(record).data
            })
        return Response(
            {'error': 'Record is not deleted'},
            status=status.HTTP_400_BAD_REQUEST
        )