# this file is made for giving each page in the site a context, namely, we can use this context in each template in the app
# we can call this file any name we want
# [Note: the context is like the dictionary we pass to render() function (for example: {'categories': categories})]

from store.models import Category, Cart, Product


# we can call this function any name we want
def store_website(request):
    cart = Cart.objects.filter(session=request.session.session_key).last()

    cart_total = 0
    cart_products = []

    if cart:
        cart_products = Product.objects.filter(pk__in=cart.items)
        for item in cart_products:
            cart_total += item.price

    categories = Category.objects.order_by('order')
    return {
        'categories': categories,
        'cart_products': cart_products,
        'cart_total': cart_total
        }