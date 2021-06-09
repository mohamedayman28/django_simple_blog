"""
Module for repeated objects used within views.
"""

# Django
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def pagination(request, queryset, objects_per_page):
    """
    Return paginated queryset according to the number passed to
    objects_per_page argument.

    Workd only within a function view or class based view method with request
    argument passed to it.
    """

    paginator = Paginator(queryset, objects_per_page)
    page = request.GET.get('page')
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        # Last page.
        paginated_queryset = paginator.page(paginator.num_pages)

    return paginated_queryset
