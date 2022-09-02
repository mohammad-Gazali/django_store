from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Category, Product, Slider

# Create your views here.

def index(request):
    products = Product.objects.select_related('author').filter(featured=True)
    slides = Slider.objects.order_by('order')
    return render(
        request, 
        "index.html",
        {
            "products": products,
            "slides": slides
        }
    )


def product(request, pid):
    return render(request, "product.html")


def category(request, cid=None):
    cat = None
    where = {}
    query = request.GET.get('q')
    cid = request.GET.get('category_from_select', cid)  # the second parameter here in get() function is the default value to cid if 'category_from_select' isn't exist
    if cid:
        cat = Category.objects.get(pk=cid)
        where['category_id'] = cid

    if query:
        where['name__icontains'] = query

    products = Product.objects.filter(**where)
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(page_obj.paginator.count)
    return render(
        request, "category.html", {
            'category': cat,
            'page_obj': page_obj
        }
    )
    


def cart(request):
    return render(request, "cart.html")


def checkout(request):
    return render(request, "checkout.html")


def checkout_complete(request):
    return render(request, "checkout-complete.html")