from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

TICKET_W = 255
TICKET_H = 155
COLS     = 2
MARGIN_X = 20
MARGIN_Y = 20
GAP_X    = 10
GAP_Y    = 10


class TicketPDFGenerator:

    @classmethod
    def generate_batch(cls, tickets):
        buffer  = BytesIO()
        c       = canvas.Canvas(buffer, pagesize=A4)
        pw, ph  = A4
        x_pos   = [MARGIN_X, MARGIN_X + TICKET_W + GAP_X]
        y_start = ph - MARGIN_Y - TICKET_H
        col, y  = 0, y_start

        for ticket in tickets:
            cls._draw_ticket(c, x_pos[col], y, ticket)
            col += 1
            if col >= COLS:
                col  = 0
                y   -= (TICKET_H + GAP_Y)
                if y < MARGIN_Y:
                    c.showPage()
                    y = y_start

        c.save()
        buffer.seek(0)
        return buffer

    @classmethod
    def generate_ticket(cls, ticket):
        return cls.generate_batch([ticket])

    @classmethod
    def _draw_ticket(cls, c, x, y, ticket):
        # Border
        c.setStrokeColor(colors.HexColor("#1a3a5c"))
        c.setLineWidth(1.5)
        c.roundRect(x, y, TICKET_W, TICKET_H, 8, stroke=1, fill=0)

        # Header band
        c.setFillColor(colors.HexColor("#1a3a5c"))
        c.roundRect(x, y + TICKET_H - 36, TICKET_W, 36, 8, stroke=0, fill=1)
        c.rect(x, y + TICKET_H - 36, TICKET_W, 18, stroke=0, fill=1)

        # Church name
        c.setFillColor(colors.HexColor("#e8a020"))
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(x + TICKET_W / 2, y + TICKET_H - 22, "KAG CLAY WORKS — RAFFLE DRAW")

        # Ticket number
        c.setFillColor(colors.HexColor("#1a3a5c"))
        c.setFont("Helvetica-Bold", 36)
        c.drawCentredString(x + TICKET_W / 2, y + TICKET_H - 76, f"#{ticket.formatted_number}")

        # Divider
        c.setStrokeColor(colors.HexColor("#d1d5db"))
        c.setLineWidth(0.5)
        c.line(x + 12, y + TICKET_H - 86, x + TICKET_W - 12, y + TICKET_H - 86)

        # Details
        c.setFillColor(colors.HexColor("#1a1a2e"))
        c.setFont("Helvetica", 8)
        c.drawString(x + 14, y + TICKET_H - 100, f"Name:  {ticket.member.name}")
        c.drawString(x + 14, y + TICKET_H - 114, f"Event: {ticket.event.name}")
        c.drawString(x + 14, y + TICKET_H - 128, f"Draw:  {ticket.event.draw_date.strftime('%d %B %Y')}")

        # Ref
        c.setFillColor(colors.HexColor("#6b7280"))
        c.setFont("Helvetica", 7)
        c.drawRightString(x + TICKET_W - 14, y + 8, f"Ref: {ticket.payment.bank_reference}")
