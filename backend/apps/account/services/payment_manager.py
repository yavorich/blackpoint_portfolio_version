from django.utils.timezone import localtime
from config.settings import PAYMENT_TEST_MODE
from core.singleton import SingletonMeta
from apps.account.services.payment_api import PaykeeperPaymentApi
from apps.account.models import SubscriptionPayment
from apps.account.tasks import (
    expire_subscription_payment,
    confirm_user_subscription_payment,
)


class PaymentManager(metaclass=SingletonMeta):
    payment_api = PaykeeperPaymentApi()

    def buy(self, data, user):
        payment = SubscriptionPayment.objects.create(
            user=user,
            price=data["tariff"].price,
            status=SubscriptionPayment.Status.PENDING,
            **data,
        )
        payment_data = self.payment_api.init_payment(payment)
        for attr, value in payment_data.items():
            setattr(payment, attr, value)

        payment.save()

        if PAYMENT_TEST_MODE:
            payment.status = SubscriptionPayment.Status.SUCCESS
            payment.payment_date = localtime()
            payment.save()

            confirm_user_subscription_payment.apply_async(
                args=[payment.uuid], countdown=3
            )

        else:
            expire_subscription_payment.apply_async(
                args=[payment.uuid], eta=payment_data["expiry_datetime"]
            )
        return payment_data
