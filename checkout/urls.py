from django.urls import path
from . import views
from . import webhooks

urlpatterns = [
    path('stripe/config', views.stripe_config, name="checkout.stripe.config"),
    path('stripe/webhook', webhooks.stripe_webhook, name="checkout.stripe.webhook"),
    path('stripe', views.stripe_transaction, name="checkout.stripe"),
    path('paypal', views.paypal_transaction, name="checkout.paypal"),
]