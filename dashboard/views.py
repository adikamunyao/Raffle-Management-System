# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from payments.models import Payment
from tickets.models import Ticket
from django.contrib import messages
from dashboard.forms import SMSForm
from payments.services.sms_processor import SMSProcessor

@login_required
def dashboard_home(request):

    context = {
        "total_payments": Payment.objects.count(),
        "total_tickets": Ticket.objects.count(),
        "latest_payments": Payment.objects.select_related("member").order_by("-id")[:10],
        "latest_tickets": Ticket.objects.select_related("member").order_by("-id")[:10],
    }

    return render(request, "dashboard/home.html", context)

@login_required
def submit_sms(request):

    form = SMSForm()

    if request.method == "POST":

        form = SMSForm(request.POST)

        if form.is_valid():

            try:

                result = SMSProcessor.process(
                    sms_text=form.cleaned_data["sms_text"],
                    phone_number=form.cleaned_data["phone_number"],
                    event=form.cleaned_data["event"],
                    user=request.user
                )

                messages.success(
                    request,
                    f"Success! {len(result['tickets'])} tickets generated."
                )

                return render(
                    request,
                    "dashboard/result.html",
                    result
                )

            except Exception as e:

                messages.error(request, str(e))

    return render(
        request,
        "dashboard/submit_sms.html",
        {"form": form}
    )