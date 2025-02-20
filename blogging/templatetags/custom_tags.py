from django import template
from django.utils.translation import get_language
register = template.Library()
from django.conf import settings

@register.simple_tag
def get_url_tag(request, lang):
    if lang:
        active_language = get_language()
        return request.path.replace(active_language, lang, 1)
    return request.path

@register.simple_tag
def get_title(language):
    for code, title in settings.LANGUAGES:
        if code == language:
            return title
    return None