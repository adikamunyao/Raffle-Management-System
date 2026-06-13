# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Prize
from .services.draw_engine import DrawEngine


@login_required
def draw_prize(request, prize_id):

    prize = get_object_or_404(Prize, pk=prize_id)

    try:
        winner = DrawEngine.draw_prize(prize.event, prize)
        messages.success(request, f"Winner: {winner.ticket.member.name}")
    except Exception as e:
        messages.error(request, str(e))

    return redirect("draw_panel", event_id=prize.event_id)


@login_required
@require_POST
def draw_winner_api(request, prize_id):

    prize = get_object_or_404(Prize.objects.select_related("event"), id=prize_id)

    try:
        winner = DrawEngine.draw_prize(event=prize.event, prize=prize)
        return JsonResponse({
            "status": "success",
            "winner_name": winner.ticket.member.name,
            "ticket_number": winner.ticket.formatted_number,
            "prize": prize.name
        })
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@login_required
def draw_panel(request, event_id):
    prizes = Prize.objects.filter(event_id=event_id)
    return render(request, "prizes/draw_panel.html", {"prizes": prizes})


@login_required
def live_draw_screen(request, prize_id):
    prize = get_object_or_404(Prize, id=prize_id)
    return render(request, "prizes/live_draw.html", {"prize": prize})