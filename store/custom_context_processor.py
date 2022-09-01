# this file is made for giving each page in the site a context, namely, we can use this context in each template in the app
# we can call this file any name we want
# [Note: the context is like the dictionary we pass to render() function (for example: {'categories': categories})]

from store.models import Category


# we can call this function any name we want
def store_website(request):
    categories = Category.objects.order_by('order')
    return {'categories': categories}