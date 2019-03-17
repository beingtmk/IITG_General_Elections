from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='splitter')
@stringfilter
def splitter(value): # Only one argument.
	print(value)
	return value.split(':')

@stringfilter
def str_lower(value):
	return value.lower()
