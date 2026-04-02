from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FinancialRecordViewSet

router = DefaultRouter()
router.register(r'', FinancialRecordViewSet, basename='financialrecord')

urlpatterns = [
    path('', include(router.urls)),
]   