from django import template
import math
register = template.Library()

@register.filter(name='show_discounted_price')
def show_discounted_price(sale_price, discount):
    final_amount = sale_price*(1+(discount/100))
    return math.floor(final_amount)
