from django.db import transaction

from members.models import Member
from payments.models import Payment
from payments.services.sms_parser import CoopBankSMSParser, SMSParserError
from payments.services.payment_processor import PaymentProcessor


class SMSProcessorError(Exception):
    pass


class SMSProcessor:

    @classmethod
    @transaction.atomic
    def process(cls, *, sms_text, member, event, user, chosen_numbers):

        parsed = CoopBankSMSParser.parse(sms_text)

        # Update member name from SMS if it was not set
        if parsed["name"] and not member.name:
            member.name = parsed["name"]
            member.save(update_fields=["name"])

        if Payment.objects.filter(bank_reference=parsed["bank_reference"]).exists():
            raise SMSProcessorError(
                f"Transaction {parsed['bank_reference']} has already been processed."
            )

        payment = Payment.objects.create(
            event=event,
            member=member,
            amount=parsed["amount"],
            bank_reference=parsed["bank_reference"],
            sms_text=sms_text,
            processed_by=user,
            status=Payment.VERIFIED,
        )

        tickets = PaymentProcessor.process(payment, chosen_numbers)

        return {
            "member":  member,
            "payment": payment,
            "tickets": tickets,
        }
