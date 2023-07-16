from django.shortcuts import render


def page_not_found(request, exception):
    """Выдаёт кастомный шаблон на ошибку 404."""
    return render(request, 'core/404.html', {'path': request.path}, status=404)


def csrf_failure(request, reason=''):
    """Выдаёт кастомный шаблон на ошибку 403."""
    return render(request, 'core/403csrf.html')
