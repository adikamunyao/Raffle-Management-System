import secrets
from django.db import transaction

from prizes.models import Winner
from tickets.models import Ticket


class DrawError(Exception):
    pass


class DrawEngine:

    @classmethod
    @transaction.atomic
    def draw_prize(cls, event, prize):

        if Winner.objects.filter(prize=prize).count() >= prize.quantity:
            raise DrawError("Prize already completed")

        used_ticket_ids = Winner.objects.filter(
            event=event
        ).values_list("ticket_id", flat=True)

        eligible_tickets = Ticket.objects.filter(
            event=event
        ).exclude(id__in=used_ticket_ids)

        if not eligible_tickets.exists():
            raise DrawError("No tickets available")

        winner_ticket = secrets.choice(list(eligible_tickets))

        winner = Winner.objects.create(
            event=event,
            prize=prize,
            ticket=winner_ticket
        )

        winner_ticket.status = Ticket.WON
        winner_ticket.save(update_fields=["status"])

        return winner