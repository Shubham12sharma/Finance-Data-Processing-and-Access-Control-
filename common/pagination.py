from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound

class StandardResultsSetPagination(PageNumberPagination):
    
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        try:
            return super().paginate_queryset(queryset, request, view)
        except NotFound:
            # Return last page instead of 404
            page_number = self.get_page_number(request, queryset)
            if page_number > 1:
                # Force to last page
                request.query_params._mutable = True
                request.query_params['page'] = self.page.paginator.num_pages
                ret