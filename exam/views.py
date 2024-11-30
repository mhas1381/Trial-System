from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
import json
from datetime import timedelta
from .models import TabChange
# Create your views here.


def exam_view(request):

    return render(request, "exam/exam.html")


def home_view(request):
    return render(request, 'home.html')


@csrf_exempt
def track_tab_change(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        ip_address = request.META.get('REMOTE_ADDR')
        user = request.user

        if not user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=403)

        if action in ['tab-hidden', 'tab-visible', 'mouse-left', 'mouse-entered']:
            tab_change, created = TabChange.objects.get_or_create(user=user)
            tab_change.add_tab_change(action, user_agent, ip_address)

            # Print the event in the terminal
            if action == 'tab-hidden':
                print(f"User hide the tab.")
            elif action == 'tab-visible':
                print(f"User returned to the tab.")
            elif action == 'mouse-left':
                print(f"User moved the mouse out of the window.")
            elif action == 'mouse-entered':
                print(f"User moved the mouse back into the window.")

            # Check the number of tab changes
            tab_change_count = tab_change.count_tab_changes()
            if tab_change_count == 40:
                # Send a warning message
                return JsonResponse({'status': 'warning', 'message': 'شما ۲۰ بار از صفحه آزمون خارج شده اید.'})
            
            total_time_away = tab_change.calculate_total_time_away()
            print(total_time_away)
            
            if total_time_away > timedelta(seconds=500):
                return JsonResponse({'status': 'warning', 'message': 'شما برای مدت زیادی از صفحه آزمون خارج شده اید!'})
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
