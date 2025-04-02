from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def css_file():
    if settings.DEBUG:
        return 'css/output.css'
    else:
        return 'css/minify.css'
