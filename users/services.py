import requests
from django.conf import settings
from rest_framework import status
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def convert_currencies(rub_price):
    usd_price = 0
    response = requests.get(
        f'{settings.CUR_API_URL}v3/latest?apikey={settings.CUR_API_KEY}&currencies=RUB'
    )
    if response.status_code == status.HTTP_200_OK:
        usd_rate = response.json()['data']['RUB']['value']
        usd_price = rub_price / usd_rate

    return usd_price


def create_stripe_product(name):
    """
    Создает продукт в Stripe.
    """
    product = stripe.Product.create(name=name)
    return product.id


def create_stripe_price(product_id, amount_in_usd):
    """ Создает цену для продукта в Stripe. """
    price = stripe.Price.create(
        currency="usd",
        unit_amount=int(amount_in_usd * 100),
        product=product_id,
    )
    return price


def create_stripe_session(price):
    """ Создает сессию на оплату в Stripe. """
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
    )
    return session.id, session.url
