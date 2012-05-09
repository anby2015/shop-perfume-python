from django import template

register = template.Library()

def __isOdd(num):
    return num & 1 and True or False

@register.filter
def get_odd_even(value):
    if __isOdd(value):
        return 'odd'
    else:
        return 'even'

@register.filter(is_safe=True)
def get_sub_list(value, arg):
    arg *= 3
    lstSize = len(value)
    endIndex = arg + 3
    if lstSize < arg + 3:
        endIndex = lstSize
    return value._result_cache[arg : endIndex]

@register.filter(is_safe=True)
def get_split_list(value, arg):
    return value[::arg]

@register.filter
def get_first_last(value, arg):
    index = value.index(arg)
    if not index:
        return 'first'
    if index == len(value) - 1:
        return 'last'
    return ''

@register.filter
def get_add(value, arg):
    return value + arg

@register.filter
def get_mul(value, arg):
    return value * arg

@register.filter
def get_split_and_range(value, arg):
    return range(len(value[::arg]))

@register.filter
def new_list(value):
    lst = []
    for obj in value:
        lst.append(obj)
    return lst

