from decimal import Decimal
from django.db import transaction

from payments.models import Payment, WalletTransaction
from tickets.services.ticket_generator import TicketGenerator


class PaymentProcessorError(Exception):
    pass


class PaymentProcessor:

    @classmethod
    @transaction.atomic
    def process(cls, payment, chosen_numbers: list):
        event = payment.event
        ticket_price = event.ticket_price
        ticket_count = int(payment.amount // ticket_price)

        if ticket_count <= 0:
            raise PaymentProcessorError(
                f"Payment of KSh {payment.amount} is below the ticket price of KSh {ticket_price}."
            )

        if len(chosen_numbers) != ticket_count:
            raise PaymentProcessorError(
                f"You must choose exactly {ticket_count} ticket number(s) based on the verified payment amount."
            )

        ticket_cost = ticket_price * ticket_count
        raw_amount = payment.amount

        payment.status = Payment.VERIFIED
        payment.save(update_fields=["status"])

        # Record wallet credit for full payment amount first,
        # then debit the ticket cost to keep a clear ledger.
        balance_before = payment.member.wallet_balance
        balance_after_credit = balance_before + raw_amount
        WalletTransaction.objects.create(
            member=payment.member,
            event=event,
            payment=payment,
            amount=raw_amount,
            transaction_type=WalletTransaction.CREDIT,
            description=f"Payment received ({payment.bank_reference})",
            balance_after=balance_after_credit,
        )

        tickets = TicketGenerator.generate(payment, chosen_numbers)

        balance_after_debit = balance_after_credit - ticket_cost
        WalletTransaction.objects.create(
            member=payment.member,
            event=event,
            payment=payment,
            amount=-ticket_cost,
            transaction_type=WalletTransaction.DEBIT,
            description=f"Ticket allocation for {ticket_count} ticket(s)",
            balance_after=balance_after_debit,
        )

        payment.member.wallet_balance = balance_after_debit
        payment.member.save(update_fields=["wallet_balance"])

        return tickets
