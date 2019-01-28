from django import template

register = template.Library()

@register.filter(name='concat_pers')
def concat_pers(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2+1)


@register.filter(name='concat')
def concat(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)