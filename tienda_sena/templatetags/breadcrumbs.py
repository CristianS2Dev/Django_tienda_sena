from django import template

register = template.Library()

@register.inclusion_tag('partials/breadcrumbs.html')
def render_breadcrumbs(crumbs):
    """
    crumbs: Lista de tuplas [(nombre, url), ...]
    """
    return {'breadcrumbs': crumbs}
