from core.singleton import SingletonMeta
from apps.account.services.payment_api import PaykeeperPaymentApi
from apps.account.models import SubscriptionPayment


class PaymentManager(metaclass=SingletonMeta):
    payment_api = PaykeeperPaymentApi()

    def buy(self, place, tariff, user):
        payment = SubscriptionPayment.objects.create(
            user=user,
            place=place,
            tariff=tariff,
            price=1,  # tariff.price
        )
        payment_data = self.payment_api.init_payment(payment)
        for attr, value in payment_data.items():
            setattr(payment, attr, value)

        payment.save()
        return payment_data
