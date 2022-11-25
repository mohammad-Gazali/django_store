from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django_store.settings import STRIPE_ENDPOINT_SECRET
from .models import Transaction
from store.models import Order, Product
import stripe


@csrf_exempt  # this decorator deactivate the csrf_token in this view because that the request is coming from stripe
def stripe_webhook(request):
    event = None
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_ENDPOINT_SECRET
        )
    except ValueError:
        print("Invalid payload")
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError:
        print("Invalid signature")
        return HttpResponse(status=400)


    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event.data.object
        print("payment_intent.succeeded")
        transaction_id = payment_intent.metadata.transaction
        make_order(transaction_id)

    else:
      print('Unhandled event type {}'.format(event['type']))
    
    return HttpResponse(status=200)



def make_order(tid):
    transaction = Transaction.objects.get(pk=tid)
    
    order = Order.objects.create(transaction_id=tid)

    products = Product.objects.filter(pk__in=transaction.items)

    for product in products:
        order.orderproduct_set.create(product_id=product.id, price=product.price) #! Notice here we used created directly without "objects" property
    
    send_order_email(order, products)

    return redirect("store.checkout_complete")


def send_order_email(order, products):

    msg_html = render_to_string('emails/order.html', {'order': order, 'products': products})
    send_mail(
        subject='New Order',  
        html_message=msg_html,
        message=msg_html,
        from_email='gazaliRebly@example.com',
        recipient_list= [order.transaction.customer_email]
    )