from django import template

# in this file we have made a new filter for django templates


register = template.Library()


def currency(amount):
    return "{:.2f}".format(amount) + " $"


register.filter("currency", currency)
