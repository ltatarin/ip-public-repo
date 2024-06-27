from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def check_current_page(context, value):
    if context['current_page'] == value:
        return 'active'