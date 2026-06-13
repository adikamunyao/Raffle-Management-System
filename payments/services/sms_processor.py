from django.db import transaction

from members.models import Member
from payments.models import Payment

from payments.services.sms_parser import (
    MpesaSMSParser
)

from payments.services.payment_processor import (
    PaymentProcessor
)

class SMSProcessorError(Exception):
    pass


class SMSProcessor:

    @classmethod
    @transaction.atomic
    def process(
        cls,
        *,
        sms_text,
        phone_number,
        event,
        user
    ):

        parsed = MpesaSMSParser.parse(
            sms_text
        )

        member, _ = Member.objects.get_or_create(
            phone_number=phone_number,
            defaults={
                "name": parsed["name"]
            }
        )

        if Payment.objects.filter(
            mpesa_reference=parsed["mpesa_reference"]
        ).exists():

            raise SMSProcessorError(
                "This M-Pesa reference has already been used."
            )

        payment = Payment.objects.create(
            event=event,
            member=member,
            amount=parsed["amount"],
            mpesa_reference=parsed["mpesa_reference"],
            sms_text=sms_text,
            processed_by=user,
            status=Payment.VERIFIED
        )

        tickets = PaymentProcessor.process(
            payment
        )

        return {
            "member": member,
            "payment": payment,
            "tickets": tickets
        }