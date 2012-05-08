from django import template

register = template.Library()

def __isOdd(num):
    return num & 1 and True or False

@register.tag("getOldEven")
def get_odd_even(value):
    if __isOdd(value):
        return 'odd'
    else:
        return 'even'

@register.tag("getSubList")
def get_sub_list(value, arg):
    return value[arg]

@register.tag
def len(value):
    return len(value)

@register.tag
def range(value):
    return range(value)

@register.tag
def get_first_last(value, arg):
    if value == arg[0]:
        return 'first'
    if value == len(arg):
        return 'last'
    return ''

@register.tag
def add(value, arg):
    return value + arg

@register.tag
def mul(value, arg):
    return value * arg

