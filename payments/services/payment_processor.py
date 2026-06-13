from django.db import transaction

from payments.models import Payment
from tickets.services.ticket_generator import (
    TicketGenerator
)


class DuplicateMpesaReference(Exception):
    pass


class PaymentProcessor:

    @classmethod
    @transaction.atomic
    def process(cls, payment):

        if Payment.objects.filter(
            mpesa_reference=payment.mpesa_reference
        ).exclude(
            id=payment.id
        ).exists():

            raise DuplicateMpesaReference(
                "Duplicate reference."
            )

        payment.status = Payment.VERIFIED
        payment.save()

        tickets = TicketGenerator.generate(
            payment
        )

        return tickets