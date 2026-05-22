from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiply value by arg"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def add(value, arg):
    """Add value and arg"""
    try:
        return float(value) + float(arg)
    except (ValueError, TypeError):
        return 0
