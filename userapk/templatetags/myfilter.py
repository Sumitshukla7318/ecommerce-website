from django import template
register=template.Library()

@register.filter
def mul(price, quantity):
    return price * quantity


@register.filter
def subtotal(cart_items):
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    return subtotal

@register.filter
def in_cart(id):
    print(id)
    return True

@register.filter
def get_cart_items(cart_items):
    return [item.product for item in cart_items]

