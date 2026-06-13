from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django import forms

from events.models import RaffleEvent
from members.models import Member
from payments.models import Payment
from payments.services.sms_parser import CoopBankSMSParser, SMSParserError
from payments.services.sms_processor import SMSProcessor
from tickets.models import Ticket


class MemberSignupForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ["name", "phone_number"]
        widgets = {
            "name":         forms.TextInput(attrs={"placeholder": "e.g. John Kamau"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "e.g. 0712345678"}),
        }


# ── Step 1: Register ──────────────────────────────────────────────────────────

def signup(request):
    form = MemberSignupForm()
    if request.method == "POST":
        form = MemberSignupForm(request.POST)
        if form.is_valid():
            member = form.save()
            request.session["member_id"]   = member.id
            request.session["member_name"] = member.name
            return redirect("payment_instructions")
    return render(request, "members/signup.html", {"form": form})


# ── Step 2: Payment Instructions ──────────────────────────────────────────────

def payment_instructions(request):
    event = RaffleEvent.objects.filter(status=RaffleEvent.ACTIVE).first()
    return render(request, "members/payment_instructions.html", {"event": event})


# ── Step 3a: Paste SMS → parse & show ticket count ───────────────────────────

def submit_payment(request):
    member_id = request.session.get("member_id")
    if not member_id:
        return redirect("member_signup")

    member = get_object_or_404(Member, id=member_id)
    event  = RaffleEvent.objects.filter(status=RaffleEvent.ACTIVE).first()

    if not event:
        messages.error(request, "No active raffle event. Please check back later.")
        return redirect("payment_instructions")

    taken     = set(Ticket.objects.filter(event=event).values_list("ticket_number", flat=True))
    available = [n for n in range(1, event.max_ticket_number + 1) if n not in taken]

    # Stage 2: member confirms chosen numbers → save
    if request.method == "POST" and "confirm" in request.POST:
        sms_text   = request.POST.get("sms_text", "").strip()
        chosen_raw = request.POST.getlist("ticket_numbers")

        try:
            chosen_numbers = [int(n) for n in chosen_raw]
        except ValueError:
            messages.error(request, "Invalid ticket numbers submitted.")
            return redirect("submit_payment")

        try:
            result = SMSProcessor.process(
                sms_text=sms_text,
                member=member,
                event=event,
                user=None,
                chosen_numbers=chosen_numbers,
            )
            request.session["last_payment_id"] = result["payment"].id
            return redirect("member_result")
        except Exception as e:
            messages.error(request, str(e))
            # Re-show choose screen
            try:
                parsed       = CoopBankSMSParser.parse(sms_text)
                ticket_count = int(parsed["amount"] / event.ticket_price)
                return render(request, "members/choose_tickets.html", {
                    "member": member, "event": event, "parsed": parsed,
                    "ticket_count": ticket_count, "sms_text": sms_text,
                    "available": available, "taken": sorted(taken),
                    "max_num": event.max_ticket_number,
                })
            except Exception:
                pass

    # Stage 1: parse SMS → show ticket count + number picker
    if request.method == "POST" and "sms_text" in request.POST:
        sms_text = request.POST.get("sms_text", "").strip()
        try:
            parsed       = CoopBankSMSParser.parse(sms_text)
            ticket_count = int(parsed["amount"] / event.ticket_price)

            if ticket_count <= 0:
                messages.error(
                    request,
                    f"Payment of KSh {parsed['amount']} is below the ticket "
                    f"price of KSh {event.ticket_price}."
                )
            else:
                return render(request, "members/choose_tickets.html", {
                    "member":       member,
                    "event":        event,
                    "parsed":       parsed,
                    "ticket_count": ticket_count,
                    "sms_text":     sms_text,
                    "available":    available,
                    "taken":        sorted(taken),
                    "max_num":      event.max_ticket_number,
                })
        except SMSParserError as e:
            messages.error(request, str(e))

    return render(request, "members/submit_payment.html", {
        "member":    member,
        "event":     event,
        "available": available,
        "taken":     sorted(taken),
    })


# ── Result ────────────────────────────────────────────────────────────────────

def member_result(request):
    payment_id = request.session.get("last_payment_id")
    if not payment_id:
        return redirect("member_signup")

    payment = get_object_or_404(
        Payment.objects.select_related("member", "event"), id=payment_id
    )
    tickets = list(payment.tickets.all().order_by("ticket_number"))

    return render(request, "members/result.html", {
        "payment": payment,
        "member":  payment.member,
        "tickets": tickets,
    })
