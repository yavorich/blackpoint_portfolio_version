from celery import shared_task
from django.utils.timezone import localdate, timedelta

from apps.account.models import SubscriptionPayment, BaseSubscription, UserSubscription


@shared_task
def apply_user_subscription_payment(payment_id):
    payment = SubscriptionPayment.objects.filter(id=payment_id).first()
    if not payment:
        return "Платёж не найден"

    base_subscription = BaseSubscription.objects.first()
    user_subscription = UserSubscription.objects.filter(
        user=payment.user, place=payment.place
    ).first()
    if user_subscription:
        user_subscription.expire_date = max(
            localdate(), user_subscription.expire_date
        ) + timedelta(days=base_subscription.duration_days)
        user_subscription.save()
    else:
        user_subscription = UserSubscription.objects.create(
            user=payment.user,
            place=payment.place,
            expire_date=localdate() + timedelta(days=base_subscription.duration_days),
        )
