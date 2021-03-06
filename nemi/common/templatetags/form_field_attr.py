'''
Created on Feb 10, 2012

@author: mbucknel
'''

from django import template


register = template.Library()


@register.filter(name='tooltip', is_safe=True)
def tooltip(field):
    try:
        return field.form.fields[field.name].tooltip
    except AttributeError:
        return ''
