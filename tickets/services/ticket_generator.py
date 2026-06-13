from django.db import transaction
from tickets.models import Ticket


class TicketGenerationError(Exception):
    pass


class TicketGenerator:

    @classmethod
    @transaction.atomic
    def generate(cls, payment, chosen_numbers: list):

        if payment.tickets.exists():
            raise TicketGenerationError(
                "Tickets have already been generated for this payment."
            )

        if payment.status != Payment.VERIFIED:
            raise TicketGenerationError(
                "Only verified payments can generate tickets."
            )

        ticket_price = payment.event.ticket_price
        ticket_count = int(payment.amount / ticket_price)

        if ticket_count <= 0:
            raise TicketGenerationError(
                f"Payment of KSh {payment.amount} is below the ticket "
                f"price of KSh {ticket_price}."
            )

        if len(chosen_numbers) != ticket_count:
            raise TicketGenerationError(
                f"You must choose exactly {ticket_count} ticket number(s) "
                f"based on your payment of KSh {payment.amount}."
            )

        if len(chosen_numbers) != len(set(chosen_numbers)):
            raise TicketGenerationError("You selected duplicate ticket numbers.")

        max_num = payment.event.max_ticket_number
        for num in chosen_numbers:
            if not (1 <= num <= max_num):
                raise TicketGenerationError(
                    f"Ticket {num} is out of range. Choose between 1 and {max_num}."
                )

        # Lock rows to prevent race condition
        taken = set(
            Ticket.objects.select_for_update()
            .filter(event=payment.event)
            .values_list("ticket_number", flat=True)
        )

        conflicts = [n for n in chosen_numbers if n in taken]
        if conflicts:
            raise TicketGenerationError(
                f"Ticket(s) {', '.join(str(n) for n in conflicts)} already taken. "
                "Please choose different numbers."
            )

        return Ticket.objects.bulk_create([
            Ticket(
                ticket_number=num,
                event=payment.event,
                member=payment.member,
                payment=payment,
            )
            for num in chosen_numbers
        ])


# avoid circular import
from payments.models import Payment  # noqa: E402
