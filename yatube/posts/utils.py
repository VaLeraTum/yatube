from django.core.paginator import Paginator

LAST_POSTS = 10


def paginator_fun(request, obj):
    """Функция для пагинация."""
    paginator = Paginator(obj, LAST_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
