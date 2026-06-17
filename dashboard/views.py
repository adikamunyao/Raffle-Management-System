from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db.models import Sum

from payments.models import Payment
from tickets.models import Ticket
from members.models import Member
from events.models import RaffleEvent
from prizes.models import Winner
from dashboard.models import LandingPageContent
from dashboard.forms import SMSForm
from payments.services.sms_parser import CoopBankSMSParser, SMSParserError
from payments.services.sms_processor import SMSProcessor


def landing(request):
    """Public landing page — info, register or pay."""
    if request.user.is_authenticated:
        from django.shortcuts import redirect
        return redirect("dashboard_home")
    content, _ = LandingPageContent.objects.get_or_create(pk=1)
    event = RaffleEvent.objects.filter(status=RaffleEvent.ACTIVE).first()
    total_tickets = Ticket.objects.count()
    total_members = Member.objects.count()
    active_event_tickets_sold = Ticket.objects.filter(event=event).count() if event else 0
    tickets_remaining = (
        max(0, event.max_ticket_number - active_event_tickets_sold)
        if event and event.max_ticket_number is not None else 0
    )
    progress_percent = (
        int(active_event_tickets_sold / event.max_ticket_number * 100)
        if event and event.max_ticket_number else 0
    )
    ticket_price = event.ticket_price if event and event.ticket_price is not None else 500
    draw_date_iso = event.draw_date.isoformat() if event and event.draw_date else ""
    return render(request, "landing.html", {
        "content":                 content,
        "event":                    event,
        "total_tickets":            total_tickets,
        "total_members":            total_members,
        "active_event_tickets_sold": active_event_tickets_sold,
        "tickets_remaining":        tickets_remaining,
        "progress_percent":         progress_percent,
        "ticket_price":             ticket_price,
        "draw_date_iso":            draw_date_iso,
    })


@login_required
def dashboard_home(request):
    active_event = RaffleEvent.objects.filter(status=RaffleEvent.ACTIVE).first()

    total_revenue = Payment.objects.filter(status=Payment.VERIFIED).aggregate(total=Sum("amount"))["total"] or 0
    total_wallet_balance = Member.objects.aggregate(total=Sum("wallet_balance"))["total"] or 0
    active_event_tickets_sold = Ticket.objects.filter(event=active_event).count() if active_event else 0
    tickets_remaining = (
        max(0, active_event.max_ticket_number - active_event_tickets_sold)
        if active_event else 0
    )

    context = {
        "total_payments":      Payment.objects.count(),
        "total_revenue":       total_revenue,
        "total_tickets":       Ticket.objects.count(),
        "total_wallet_balance": total_wallet_balance,
        "total_winners":       Winner.objects.count(),
        "active_events":       RaffleEvent.objects.filter(status=RaffleEvent.ACTIVE).count(),
        "active_event":        active_event,
        "active_event_tickets_sold": active_event_tickets_sold,
        "tickets_remaining":    tickets_remaining,
        "latest_payments":      Payment.objects.select_related("member").order_by("-id")[:10],
        "latest_tickets":       Ticket.objects.select_related("member").order_by("-id")[:10],
    }
    return render(request, "dashboard/home.html", context)


@login_required
def submit_sms(request):
    """
    Stage 1  — secretary pastes SMS + enters phone number → system parses & previews.
    Stage 2  — secretary selects ticket numbers → confirmed & saved.
    """
    form = SMSForm(request.POST or None)
    event = None

    if form.is_bound and form.is_valid():
        event = form.cleaned_data["event"]
    elif request.method == "POST" and "event" in request.POST:
        event_id = request.POST.get("event")
        event = RaffleEvent.objects.filter(id=event_id, status=RaffleEvent.ACTIVE).first()

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

        if not event:
            messages.error(request, "No active event selected. Please choose an active event.")
            return render(request, "dashboard/submit_sms.html", {
                "form":      form,
                "event":     event,
                "available": available,
                "taken":     taken,
            })

        try:
            chosen_numbers = [int(n) for n in chosen_raw]
        except ValueError:
            messages.error(request, "Invalid ticket numbers.")
            return render(request, "dashboard/submit_sms.html", {
                "form":      form,
                "event":     event,
                "available": available,
                "taken":     taken,
            })

        member = Member.objects.filter(phone_number=phone_number).order_by('id').first()
        if not member:
            member = Member.objects.create(phone_number=phone_number, name="")
        elif Member.objects.filter(phone_number=phone_number).count() > 1:
            messages.warning(
                request,
                "Multiple members exist with this phone number; using the first matched record."
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
            return render(request, "dashboard/submit_sms.html", {
                "form":      form,
                "event":     event,
                "available": [],
                "taken":     set(),
            })

        try:
            parsed       = CoopBankSMSParser.parse(sms_text)
            ticket_count = int(parsed["amount"] / event.ticket_price)

            if ticket_count <= 0:
                messages.error(
                    request,
                    f"Payment of KSh {parsed['amount']} is below the ticket price "
                    f"of KSh {event.ticket_price}."
                )
                return render(request, "dashboard/submit_sms.html", {
                    "form":      form,
                    "event":     event,
                    "available": available,
                    "taken":     taken,
                    "sms_text":  sms_text,
                    "phone_number": phone_number,
                })

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
        "form":      form,
        "event":     event,
        "available": available,
        "taken":     taken,
    })
