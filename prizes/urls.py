from django.urls import path
from . import views

app_name = "prizes"

urlpatterns = [
    path("draw/<int:prize_id>/trigger/", views.draw_prize, name="draw_prize"),
    path("draw/<int:prize_id>/", views.draw_winner_api, name="draw_winner_api"),
    path("live/<int:prize_id>/", views.live_draw_screen, name="live_draw_screen"),
    path("panel/<int:event_id>/", views.draw_panel, name="draw_panel"),
]