from django.db import transaction
from django.db.models import Max

from tickets.models import Ticket


class TicketGenerationError(Exception):
    pass


class TicketGenerator:

    @classmethod
    @transaction.atomic
    def generate(cls, payment):

        if payment.tickets.exists():
            raise TicketGenerationError(
                "Tickets have already been generated for this payment."
            )

        if payment.status != payment.VERIFIED:
            raise TicketGenerationError(
                "Only verified payments can generate tickets."
            )

        ticket_price = payment.event.ticket_price
        ticket_count = int(payment.amount / ticket_price)

        if ticket_count <= 0:
            raise TicketGenerationError(
                "Payment amount is below ticket price."
            )

        # Lock the row to prevent race conditions on concurrent requests
        last_ticket = (
            Ticket.objects.select_for_update()
            .filter(event=payment.event)
            .aggregate(Max("ticket_number"))["ticket_number__max"]
            or 0
        )

        tickets = Ticket.objects.bulk_create([
            Ticket(
                ticket_number=last_ticket + i + 1,
                event=payment.event,
                member=payment.member,
                payment=payment,
            )
            for i in range(ticket_count)
        ])

        return tickets