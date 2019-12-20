from django.template import Library


register = Library()

@register.filter
def space_to_underscore(obj):
    return obj.replace(" ", "_")