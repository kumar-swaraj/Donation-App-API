from django.urls import path

from payments import views
from payments.webhooks import stripe_webhook

app_name = 'payments'
urlpatterns = [
    path('my-donations/', view=views.my_donations),
    path('stripe/publishable-key/', view=views.get_stripe_publishable_key),
    path('stripe/create-payment-intent/', view=views.create_payment_intent),
    path('stripe/webhook/', stripe_webhook),
]
