from django.urls import path
from . import views

urlpatterns = [
    path("download/<int:payment_id>/", views.download_tickets_pdf, name="download_tickets_pdf"),
    path("print/<int:ticket_id>/",     views.print_ticket,         name="print_ticket"),
]
