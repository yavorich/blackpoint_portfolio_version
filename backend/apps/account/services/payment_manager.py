from core.singleton import SingletonMeta
from apps.account.services.payment_api import PaykeeperPaymentApi
from apps.account.models import SubscriptionPayment
from apps.account.tasks import expire_subscription_payment


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

        expire_subscription_payment.apply_async(
            args=[payment.uuid], eta=payment_data["expiry_datetime"]
        )
        return payment_data
