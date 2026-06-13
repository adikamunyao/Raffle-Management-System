from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django import forms

from .models import User, DEFAULT_PASSWORD


# ── Login / Logout ────────────────────────────────────────────────────────────

def login_view(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.must_change_password:
                return redirect("change_password")
            return redirect("dashboard_home")
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


# ── Force Password Change ─────────────────────────────────────────────────────

@login_required
def change_password(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            user.must_change_password = False
            user.save(update_fields=["must_change_password"])
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully.")
            return redirect("dashboard_home")
    return render(request, "accounts/change_password.html", {
        "form": form,
        "forced": request.user.must_change_password
    })


# ── Staff Management (Admin only) ─────────────────────────────────────────────

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin():
            messages.error(request, "Admin access required.")
            return redirect("dashboard_home")
        return view_func(request, *args, **kwargs)
    return wrapper


class CreateStaffForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "role"]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name"}),
            "username": forms.TextInput(attrs={"placeholder": "Username"}),
            "email": forms.EmailInput(attrs={"placeholder": "email@example.com"}),
        }


@login_required
@admin_required
def staff_list(request):
    staff = User.objects.all().order_by("role", "first_name")
    return render(request, "accounts/staff_list.html", {"staff": staff})


@login_required
@admin_required
def create_staff(request):
    form = CreateStaffForm()
    if request.method == "POST":
        form = CreateStaffForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(DEFAULT_PASSWORD)
            user.must_change_password = True
            user.save()
            messages.success(
                request,
                f"Account created for {user.get_full_name() or user.username}. "
                f"Default password: {DEFAULT_PASSWORD}"
            )
            return redirect("staff_list")
    return render(request, "accounts/create_staff.html", {"form": form})


@login_required
@admin_required
def reset_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.set_password(DEFAULT_PASSWORD)
    user.must_change_password = True
    user.save()
    messages.success(
        request,
        f"Password reset to default for {user.get_full_name() or user.username}."
    )
    return redirect("staff_list")
