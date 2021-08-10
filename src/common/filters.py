from rest_framework.filters import OrderingFilter


class CustomOrderingFilterBackends(OrderingFilter):
    def get_schema_fields(self, view):
        self.ordering_description = '정렬 가능한 필드: ' + ', '.join(view.ordering_fields)
        return super().get_schema_fields(view)
