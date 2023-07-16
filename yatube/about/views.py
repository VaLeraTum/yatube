from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    """Обрабатывает запрос по адрессу /author и выдаёт шаблон."""
    template_name = 'about/author.html'


class AboutTechView(TemplateView):
    """Обрабатывает запрос по адрессу /tech и выдаёт шаблон."""
    template_name = 'about/tech.html'
