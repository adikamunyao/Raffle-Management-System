import os
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import get_object_or_404

from payments.models import Payment
from .models import Ticket
from .services.pdf_generator import TicketPDFGenerator


def download_tickets_pdf(request, payment_id):
    """Member-facing: download their tickets as PDF."""
    payment = get_object_or_404(
        Payment.objects.select_related("member", "event"), id=payment_id
    )
    tickets  = list(payment.tickets.select_related("member", "event", "payment").order_by("ticket_number"))
    pdf      = TicketPDFGenerator.generate_batch(tickets)
    filename = f"tickets_{os.path.basename(payment.bank_reference)}.pdf"
    return FileResponse(pdf, as_attachment=True, filename=filename)


@login_required
def print_ticket(request, ticket_id):
    """Staff: print single ticket."""
    ticket   = get_object_or_404(Ticket.objects.select_related("member", "event", "payment"), id=ticket_id)
    pdf      = TicketPDFGenerator.generate_batch([ticket])
    filename = f"ticket_{os.path.basename(ticket.formatted_number)}.pdf"
    return FileResponse(pdf, as_attachment=False, filename=filename)
