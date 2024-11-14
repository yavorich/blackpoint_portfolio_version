from datetime import date
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from collections import OrderedDict


class PageNumberSetPagination(PageNumberPagination):
    """
    Удобный для фронта пагинатор с указанием текущей, предыдущей, следующей страниц.
    С возможностью добавления
    extra_queryset_data - различных сумм, агрегаций на основе queryset
    """

    page_size = 20
    page_size_query_param = "page_size"

    def get_extra_queryset_data(self, queryset, request):
        self.extra_data = {}

    def paginate_queryset(self, queryset, request, view=None):
        self.get_extra_queryset_data(queryset, request)
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [("count", self.page.paginator.count)]
                + [(attr, value) for attr, value in self.extra_data.items()]
                + [
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("current_page", self.page.number),
                    (
                        "next_page",
                        self.page.next_page_number() if self.page.has_next() else None,
                    ),
                    (
                        "previous_page",
                        (
                            self.page.previous_page_number()
                            if self.page.has_previous()
                            else None
                        ),
                    ),
                    ("num_pages", self.page.paginator.num_pages),
                    ("results", data),
                ]
            )
        )
