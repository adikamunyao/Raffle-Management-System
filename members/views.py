from django.shortcuts import render, redirect
from django import forms
from django.contrib import messages
from .models import Member


class MemberSignupForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ["name", "phone_number"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Full Name"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "e.g. 0712345678"}),
        }


def signup(request):
    form = MemberSignupForm()
    if request.method == "POST":
        form = MemberSignupForm(request.POST)
        if form.is_valid():
            member = form.save()
            request.session["member_id"] = member.id
            request.session["member_name"] = member.name
            return redirect("payment_instructions")
    return render(request, "members/signup.html", {"form": form})


def payment_instructions(request):
    return render(request, "members/payment_instructions.html")
