from django.urls import path
from . import views

urlpatterns = [
    path("signup/",          views.signup,               name="member_signup"),
    path("payment/",         views.payment_instructions, name="payment_instructions"),
    path("submit-payment/",  views.submit_payment,       name="submit_payment"),
    path("my-tickets/",      views.member_result,        name="member_result"),
]
