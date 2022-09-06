from .forms import UserInfoForm
from store.models import Product, Cart, Order
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string

# Create your views here.

def make_order(request):
    if request.method == 'GET':
        return redirect('store.checkout')

    form = UserInfoForm(request.POST)
    if form.is_valid():
        cart = Cart.objects.filter(session=request.session.session_key).last()
        products = Product.objects.filter(pk__in=cart.items)
        
        total = 0
        
        for item in products:
            total += item.price

        if total <= 0:
            return redirect('store.cart')
        order = Order.objects.create(customer=form.cleaned_data, total=total)
        for product in products:
            order.orderproduct_set.create(product_id=product.id, price=product.price)
            

        send_order_email(order, products)  # this function is defined below
        cart.delete()
        return redirect('store.checkout_complete')
    else:
        return redirect('store.checkout')


######## Notice that we use this function in the previous function, so un python we can use a function1 inside another function2 even this function2 is before function1 [[[[[ ONLY INSIDE THE FUNCTIONS ]]]]] ######
def send_order_email(order, products):

    # the render_to_string() function accept the email template as its first parameter, and the second parameter is the information we want to use in the template like normal render() function
    msg_html = render_to_string('emails/order.html', {'order': order, 'products': products})
    send_mail(
        subject='New Order',  # subject here refers to the title of the email
        html_message=msg_html,  # html_message here refers to the html structure of the email
        message=msg_html,  # message here refers to the text of email, but we here also use msg_html variable
        from_email='gazaliRebly@example.com',  # from_email here refers to the email of the sender of the email
        recipient_list= [order.customer['email']]  # recipient_list here refers to the emails (it is a list) of the receivers [Note: we can put more than one email, but we here use one email for customer]
    )