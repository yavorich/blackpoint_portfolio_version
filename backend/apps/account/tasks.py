from celery import shared_task
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

    active_subscriptions = UserSubscription.objects.filter(
        user=payment.user, place=payment.place, expire_date__gte=localdate()
    )

    # стакнуть абонементы с одинаковым тарифом
    if active_subscriptions.exists():
        last_subscription = active_subscriptions.latest("expire_date")
        if last_subscription.tariff == payment.tariff:
            last_subscription.expire_date += timedelta(days=payment.tariff.days)
            last_subscription.save()
            return

    start_date = (
        active_subscriptions.latest("expire_date").expire_date + timedelta(days=1)
        if active_subscriptions
        else localdate()
    )

    UserSubscription.objects.create(
        user=payment.user,
        place=payment.place,
        tariff=payment.tariff,
        start_date=start_date,
        expire_date=start_date + timedelta(days=payment.tariff.days),
        today_cups=payment.tariff.cups,
    )


@shared_task
def reset_today_cups():
    for subscription in UserSubscription.objects.filter(expire_date__gte=localdate()):
        subscription.today_cups = subscription.tariff.cups
        subscription.save()
