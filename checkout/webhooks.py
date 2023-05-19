from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django_store.settings import STRIPE_ENDPOINT_SECRET, PAYPAL_EMAIL
from .models import Transaction, TransactionStatus
from store.models import Order, Product
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
import stripe


@csrf_exempt  # this decorator deactivate the csrf_token in this view because that the request is coming from stripe
def stripe_webhook(request):
    event = None
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]

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

    if event["type"] == "payment_intent.succeeded":
        payment_intent = event.data.object
        print("payment_intent.succeeded")
        transaction_id = payment_intent.metadata.transaction
        make_order(transaction_id)

    else:
        print("Unhandled event type {}".format(event["type"]))

    return HttpResponse(status=200)


@csrf_exempt
def paypal_exempt(
    sender, **kwargs
):  # ? this function will be a complete function to "ipn" function which weused in "./urls.py"
    if sender.payment_status == ST_PP_COMPLETED:
        if sender.receiver_email != PAYPAL_EMAIL:
            return

        print("Payment was successful")
        make_order(
            sender.invoice
        )  # ?  Here we used "sender.invoice" as a param to make_order() because we set "invoice" in PayPalPaymentsForm in paypal_transaction in "./views.py" to the id of target transaction


#! This step is necessary to paypal payment process
valid_ipn_received.connect(
    paypal_exempt
)  # ? "valid_ipn_received" is built-in to paypal module, which is connect us to the function we want which is here paypal_exempt() function, but this variable (valid_ipn_received) is implemented if only the function ipn() (which we used in "./urls.py") successed


def make_order(tid):
    transaction = Transaction.objects.get(pk=tid)

    transaction.status = TransactionStatus.Completed

    transaction.save()

    order = Order.objects.create(transaction_id=tid)

    products = Product.objects.filter(pk__in=transaction.items)

    for product in products:
        order.orderproduct_set.create(
            product_id=product.id, price=product.price
        )  #! Notice here we used created directly without "objects" property

    send_order_email(order, products)

    return redirect("store.checkout_complete")


def send_order_email(order, products):

    msg_html = render_to_string(
        "emails/order.html", {"order": order, "products": products}
    )
    send_mail(
        subject="New Order",
        html_message=msg_html,
        message=msg_html,
        from_email="gazaliRebly@example.com",
        recipient_list=[order.transaction.customer_email],
    )
