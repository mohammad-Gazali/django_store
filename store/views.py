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
    if cid:
        cat = Category.objects.get(pk=cid)
        where['category_id'] = cid
    products = Product.objects.filter(**where)
    pageinator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = pageinator.get_page(page_number)
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