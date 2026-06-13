from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A6

from reportlab.pdfgen import canvas

class TicketPDFGenerator:

    @classmethod
    def generate_ticket(cls, ticket):

        buffer = BytesIO()

        pdf = canvas.Canvas(
            buffer,
            pagesize=A6
        )

        width, height = A6

        pdf.setFont(
            "Helvetica-Bold",
            16
        )

        pdf.drawString(
            40,
            height - 50,
            "RAFFLE DRAW"
        )

        pdf.setFont(
            "Helvetica",
            11
        )

        pdf.drawString(
            40,
            height - 90,
            f"Event: {ticket.event.name}"
        )

        pdf.drawString(
            40,
            height - 120,
            f"Ticket No: {ticket.formatted_number}"
        )

        pdf.drawString(
            40,
            height - 150,
            f"Owner: {ticket.member.name}"
        )

        pdf.drawString(
            40,
            height - 180,
            f"Draw Date: {ticket.event.draw_date}"
        )

        pdf.setStrokeColor(
            colors.black
        )

        pdf.rect(
            20,
            20,
            width - 40,
            height - 40
        )

        pdf.save()

        buffer.seek(0)

        return buffer