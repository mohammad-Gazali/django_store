from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.translation import gettext as _
from .models import Category, Product, Slider, Cart


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
    product = Product.objects.get(pk=pid)  # we didn't use select_related() because we display one element in the page, and this will be one query for author attributes
    return render(request, "product.html", {'product':product})


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
    return render(
        request, "category.html", {
            'category': cat,
            'page_obj': page_obj
        }
    )


def cart_update(request, pid):
    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key

    cart_model = Cart.objects.filter(session=session_id).last()
    if cart_model is None:
        cart_model = Cart.objects.create(session_id=session_id, items=[pid])
    elif pid not in cart_model.items:
        cart_model.items.append(pid)
        cart_model.save()
    return JsonResponse({
        'message': _('The product has been added to your cart'),
        'items_count': len(cart_model.items)
    })


def cart_remove(request, pid):
    session_id = request.session.session_key
    
    if not session_id:
        return JsonResponse({})

    cart_model = Cart.objects.filter(session=session_id).last()
    if cart_model is None:
        return JsonResponse({})
    elif pid in cart_model.items:
        cart_model.items.remove(pid)
        cart_model.save()
    return JsonResponse({
        'message': _('The product has been removed from your cart'),
        'items_count': len(cart_model.items)
    })


def cart(request):
    return render(request, "cart.html")


def checkout(request):
    return render(request, "checkout.html")


def checkout_complete(request):
    Cart.objects.filter(session=request.session.session_key).delete()
    return render(request, "checkout-complete.html")