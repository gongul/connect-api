from rest_framework.pagination import LimitOffsetPagination


class CustomLimitOffSetPagination(LimitOffsetPagination):
    limit_query_description = '페이지 당 반환 할 결과 수'
    offset_query_description = '결과를 반환할 초기 인덱스'
