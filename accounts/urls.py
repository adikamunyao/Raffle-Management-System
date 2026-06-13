from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("change-password/", views.change_password, name="change_password"),
    path("staff/", views.staff_list, name="staff_list"),
    path("staff/create/", views.create_staff, name="create_staff"),
    path("staff/reset/<int:user_id>/", views.reset_password, name="reset_password"),
]
