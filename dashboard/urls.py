from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard_home, name="dashboard_home"),
    path("submit-sms/", views.submit_sms, name="submit_sms"),
]