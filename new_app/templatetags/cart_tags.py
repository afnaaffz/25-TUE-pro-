from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product, cart):
    if isinstance(cart, dict):
        keys = cart.keys()
        for id in keys:
            if int(id) == product.id:
                return int(cart.get(id))
    return False
