# Django
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def pagination(request, queryset, objects_per_page):
    """Paginate post objects.

    NOTE: I didn't try to use the function to paginate other queryset other than post objects.

    Arguments:
        request -- Need to call the funtion within a view so that you would be able the pass the Django request
        queryset
        objects_per_page {int} -- How many objects need to be returned.
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
