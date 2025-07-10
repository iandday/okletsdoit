from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """
    Returns the value from a dictionary for a given key.
    Handles cases where the key might not exist by returning None.
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None
