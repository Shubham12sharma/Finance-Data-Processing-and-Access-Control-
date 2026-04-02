from rest_framework.views import APIView
from rest_framework.response import Response
from common.permissions import IsViewerOrHigher
from common.responses import api_success
from .services import get_dashboard_summary

class DashboardSummaryView(APIView):
    """
    Main dashboard summary endpoint.
    Accessible to all authenticated users (Viewer, Analyst, Admin)
    """
    permission_classes = [IsViewerOrHigher]

    def get(self, request):
        summary = get_dashboard_summary(request.user)
        return api_success(
            data=summary,
            message="Dashboard summary retrieved successfully"
        )