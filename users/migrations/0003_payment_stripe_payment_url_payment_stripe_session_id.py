# Generated by Django 5.0.6 on 2024-07-06 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='stripe_payment_url',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на оплату в Stripe'),
        ),
        migrations.AddField(
            model_name='payment',
            name='stripe_session_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Идентификатор сессии Stripe'),
        ),
    ]
