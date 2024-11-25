from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
import json
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

        if action in ['tab-hidden', 'tab-visible']:
            tab_change, created = TabChange.objects.get_or_create(user=user)
            tab_change.add_tab_change(action, user_agent, ip_address)

            # چاپ پیام دقیق تر
            if action == 'tab-hidden':
                print(f"User eft the tab")
            elif action == 'tab-visible':
                print(f"User returned to the tab")

            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)