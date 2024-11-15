from celery import shared_task
from django.db import transaction
from django.utils.timezone import localdate, timedelta

from apps.account.models import (
    SubscriptionPayment,
    UserSubscription,
)


@shared_task
def apply_user_subscription_payment(payment_id):
    payment = SubscriptionPayment.objects.filter(id=payment_id).first()
    if not payment:
        return "Платёж не найден"

    with transaction.atomic():
        last_place_subscription = UserSubscription.objects.filter(
            user=payment.user, place=payment.place, expire_date__gte=localdate()
        ).last()

        if last_place_subscription and last_place_subscription.tariff == payment.tariff:
            last_place_subscription.expire_date += timedelta(days=payment.tariff.days)
            last_place_subscription.save()
            subscription = last_place_subscription
        else:
            start_date = (
                last_place_subscription.expire_date + timedelta(days=1)
                if last_place_subscription
                else localdate()
            )
            subscription = UserSubscription.objects.create(
                user=payment.user,
                place=payment.place,
                tariff=payment.tariff,
                start_date=start_date,
                expire_date=start_date + timedelta(days=payment.tariff.days),
                today_cups=payment.tariff.cups,
            )
        payment.payment_date = localdate()
        payment.subscription = subscription
        payment.save()


@shared_task
def reset_today_cups():
    for subscription in UserSubscription.objects.filter(expire_date__gte=localdate()):
        subscription.today_cups = subscription.tariff.cups
        subscription.save()
