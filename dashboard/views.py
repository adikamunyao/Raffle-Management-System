from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from payments.models import Payment
from tickets.models import Ticket
from members.models import Member
from events.models import RaffleEvent
from dashboard.forms import SMSForm
from payments.services.sms_parser import CoopBankSMSParser, SMSParserError
from payments.services.sms_processor import SMSProcessor


def landing(request):
    """Public landing page — info, register or pay."""
    if request.user.is_authenticated:
        from django.shortcuts import redirect
        return redirect("dashboard_home")
    event = RaffleEvent.objects.filter(status=RaffleEvent.ACTIVE).first()
    total_tickets = Ticket.objects.count()
    total_members = Member.objects.count()
    return render(request, "landing.html", {
        "event":         event,
        "total_tickets": total_tickets,
        "total_members": total_members,
    })


@login_required
def dashboard_home(request):
    context = {
        "total_payments":  Payment.objects.count(),
        "total_tickets":   Ticket.objects.count(),
        "active_events":   RaffleEvent.objects.filter(status=RaffleEvent.ACTIVE).count(),
        "latest_payments": Payment.objects.select_related("member").order_by("-id")[:10],
        "latest_tickets":  Ticket.objects.select_related("member").order_by("-id")[:10],
    }
    return render(request, "dashboard/home.html", context)


@login_required
def submit_sms(request):
    """
    Stage 1  — secretary pastes SMS + enters phone number → system parses & previews.
    Stage 2  — secretary selects ticket numbers → confirmed & saved.
    """
    event = RaffleEvent.objects.filter(status=RaffleEvent.ACTIVE).first()

    taken = set(
        Ticket.objects.filter(event=event).values_list("ticket_number", flat=True)
    ) if event else set()

    available = (
        [n for n in range(1, event.max_ticket_number + 1) if n not in taken]
        if event else []
    )

    # ── Stage 2: confirm chosen numbers ──────────────────────────────────────
    if request.method == "POST" and "confirm" in request.POST:
        sms_text     = request.POST.get("sms_text", "").strip()
        phone_number = request.POST.get("phone_number", "").strip()
        chosen_raw   = request.POST.getlist("ticket_numbers")

        try:
            chosen_numbers = [int(n) for n in chosen_raw]
        except ValueError:
            messages.error(request, "Invalid ticket numbers.")
            return render(request, "dashboard/submit_sms.html",
                          {"event": event, "available": available, "taken": taken})

        member, _ = Member.objects.get_or_create(
            phone_number=phone_number,
            defaults={"name": ""}
        )

        try:
            result = SMSProcessor.process(
                sms_text=sms_text,
                member=member,
                event=event,
                user=request.user,
                chosen_numbers=chosen_numbers,
            )
            return render(request, "dashboard/result.html", result)
        except Exception as e:
            messages.error(request, str(e))

    # ── Stage 1: parse SMS and show preview ───────────────────────────────────
    if request.method == "POST" and "sms_text" in request.POST:
        sms_text     = request.POST.get("sms_text", "").strip()
        phone_number = request.POST.get("phone_number", "").strip()

        if not event:
            messages.error(request, "No active event. Ask an Admin to activate one.")
            return render(request, "dashboard/submit_sms.html",
                          {"event": None, "available": [], "taken": set()})

        try:
            parsed       = CoopBankSMSParser.parse(sms_text)
            ticket_count = int(parsed["amount"] / event.ticket_price)

            if ticket_count <= 0:
                messages.error(
                    request,
                    f"Payment of KSh {parsed['amount']} is below the ticket price "
                    f"of KSh {event.ticket_price}."
                )
                return render(request, "dashboard/submit_sms.html",
                              {"event": event, "available": available, "taken": taken,
                               "sms_text": sms_text, "phone_number": phone_number})

            return render(request, "dashboard/choose_tickets.html", {
                "event":        event,
                "parsed":       parsed,
                "ticket_count": ticket_count,
                "sms_text":     sms_text,
                "phone_number": phone_number,
                "available":    available,
                "taken":        sorted(taken),
                "max_num":      event.max_ticket_number,
            })

        except SMSParserError as e:
            messages.error(request, str(e))

    return render(request, "dashboard/submit_sms.html", {
        "event":     event,
        "available": available,
        "taken":     taken,
    })
