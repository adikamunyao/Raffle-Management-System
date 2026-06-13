from django.db import transaction

from payments.models import Payment
from tickets.services.ticket_generator import TicketGenerator


class PaymentProcessor:

    @classmethod
    @transaction.atomic
    def process(cls, payment, chosen_numbers: list):
        payment.status = Payment.VERIFIED
        payment.save(update_fields=["status"])
        return TicketGenerator.generate(payment, chosen_numbers)
