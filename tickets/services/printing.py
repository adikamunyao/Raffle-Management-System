from django.utils import timezone


class PrintingService:

    @classmethod
    def mark_printed(cls, ticket):

        ticket.status = ticket.PRINTED

        ticket.printed_at = (
            timezone.now()
        )

        ticket.save()