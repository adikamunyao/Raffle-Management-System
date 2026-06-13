from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import get_object_or_404
import os

from .models import Ticket
from .services.pdf_generator import TicketPDFGenerator


@login_required
def print_ticket(request, ticket_id):

    ticket = get_object_or_404(Ticket, id=ticket_id)

    pdf = TicketPDFGenerator.generate_ticket(ticket)

    safe_filename = f"ticket_{os.path.basename(ticket.formatted_number)}.pdf"

    return FileResponse(
        pdf,
        as_attachment=False,
        filename=safe_filename
    )