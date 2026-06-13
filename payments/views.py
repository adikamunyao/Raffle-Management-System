# Create your views here.
from django.contrib import messages
from django.shortcuts import render

from .forms import SMSSubmissionForm

from .services.sms_processor import (
    SMSProcessor
)

def submit_sms(request):

    form = SMSSubmissionForm()

    if request.method == "POST":

        form = SMSSubmissionForm(
            request.POST
        )

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
                    f"{len(result['tickets'])} tickets generated."
                )

            except Exception as e:

                messages.error(
                    request,
                    str(e)
                )

    return render(
        request,
        "payments/submit_sms.html",
        {
            "form": form
        }
    )