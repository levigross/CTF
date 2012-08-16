from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='progress_class')
@stringfilter
def progress_class(value):
    value = int(value)
    if value <= 10:
        return 'progress-info'
    elif value / 10 < 4:
        return 'progress-success'
    elif value / 10 < 6:
        return 'progress-warning'
    elif value / 10 < 8:
        return 'progress-danger'
    else:
        return 'progress-danger'
