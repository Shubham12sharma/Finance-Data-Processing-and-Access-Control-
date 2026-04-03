from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FinancialRecordViewSet

router = DefaultRouter()
router.register(r'', FinancialRecordViewSet, basename='record')

urlpatterns = [
    # Standard REST endpoints handled by router:
    # GET    /record/               - List all user's records (with pagination & filtering)
    # POST   /record/               - Create a new record
    # GET    /record/<id>/          - Retrieve a specific record
    # PUT    /record/<id>/          - Update a specific record
    # DELETE /record/<id>/          - Delete (soft delete) a specific record
    # PATCH  /record/<id>/          - Partial update a specific record
    #
    # Custom action endpoints:
    # GET    /record/stats/         - Get statistics for user's records
    #
    # Query Parameters:
    # ?page=1&page_size=10         - Pagination
    # ?record_type=income          - Filter by type (income/expense)
    # ?category=salary             - Filter by category
    # ?date_after=2024-01-01       - Filter by date range
    # ?date_before=2024-12-31
    # ?ordering=date               - Sort results
    
    path('', include(router.urls)),
]