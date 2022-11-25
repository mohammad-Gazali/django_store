from django.shortcuts import redirect
#? These imports were commented because we moved them to "./webhooks.py"
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.translation import gettext as _
from store.models import Product, Cart, Order
from django_store import settings
from .models import Transaction, PaymentMethod
from .forms import UserInfoForm
import stripe
import math



def stripe_config(request):
    return JsonResponse({
        'public_key': settings.STRIPE_PUBLISHABLE_KEY
    })


def stripe_transaction(request):
    transaction = make_transaction(request, PaymentMethod.Stripe)
    
    if not transaction:
        return JsonResponse({
            'message': _('Please enter valid information')
        }, status=400)

    stripe.api_key = settings.STRIPE_SECRET_KEY

    intent = stripe.PaymentIntent.create(
        amount=transaction.amount * 100,  # We multipliyed here by 100 because stripe work in this method [ surely the user won't pay ten times the amount :) ]
        currency=settings.CURRENCY,
        payment_method_types=['card'],
        metadata={  # in "metadata" argument we can send any data we want to stripe
            'transaction': transaction.id
        }
    )

    return JsonResponse({
        'client_secret': intent['client_secret']
    })

def paypal_transaction(request):
    transaction = make_transaction(request, PaymentMethod.Paypal)


def make_transaction(request, pm):
    form = UserInfoForm(request.POST)
    if form.is_valid():
        cart = Cart.objects.filter(session=request.session.session_key).last()
        products = Product.objects.filter(pk__in=cart.items)
        
        total = 0
        
        for item in products:
            total += item.price

        if total <= 0:
            return None

        return Transaction.objects.create(
            customer=form.cleaned_data, 
            session=request.session.session_key,
            payment_method=pm,
            items=cart.items,
            amount=math.floor(total)
        )


#? This function used before creating make_transaction() function above
# def make_order(request):
#     if request.method == 'GET':
#         return redirect('store.checkout')

#     form = UserInfoForm(request.POST)
#     if form.is_valid():
#         cart = Cart.objects.filter(session=request.session.session_key).last()
#         products = Product.objects.filter(pk__in=cart.items)
        
#         total = 0
        
#         for item in products:
#             total += item.price

#         if total <= 0:
#             return redirect('store.cart')
#         order = Order.objects.create(customer=form.cleaned_data, total=total)
#         for product in products:
#             order.orderproduct_set.create(product_id=product.id, price=product.price)  #! Notice here we used created directly without "objects" property
            

#         send_order_email(order, products)  # this function is defined below
#         cart.delete()
#         return redirect('store.checkout_complete')
#     else:
#         return redirect('store.checkout')


#? This function was commented because we moved it to "./webhooks.py"
######## Notice that we use this function in the previous function, so un python we can use a function1 inside another function2 even this function2 is before function1 [[[[[ ONLY INSIDE THE FUNCTIONS ]]]]] ######
# def send_order_email(order, products):

#     # the render_to_string() function accept the email template as its first parameter, and the second parameter is the information we want to use in the template like normal render() function
#     msg_html = render_to_string('emails/order.html', {'order': order, 'products': products})
#     send_mail(
#         subject='New Order',  # subject here refers to the title of the email
#         html_message=msg_html,  # html_message here refers to the html structure of the email
#         message=msg_html,  # message here refers to the text of email, but we here also use msg_html variable
#         from_email='gazaliRebly@example.com',  # from_email here refers to the email of the sender of the email
#         recipient_list= [order.customer['email']]  # recipient_list here refers to the emails (it is a list) of the receivers [Note: we can put more than one email, but we here use one email for customer]
#     )