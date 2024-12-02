from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
import json
from datetime import timedelta
from .models import *
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

        # بررسی ورود کاربر
        if not user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=403)

        # ذخیره تغییر تب یا حرکت ماوس
        if action in ['tab-hidden', 'tab-visible', 'mouse-left', 'mouse-entered']:
            tab_change, created = TabChange.objects.get_or_create(user=user)

            # افزودن تغییر تب
            tab_change.add_tab_change(action, user_agent, ip_address)

            # نمایش تغییرات در کنسول
            if action == 'tab-hidden':
                print("User hide the tab.")
            elif action == 'tab-visible':
                print("User returned to the tab.")
            elif action == 'mouse-left':
                print("User moved the mouse out of the window.")
            elif action == 'mouse-entered':
                print("User moved the mouse back into the window.")

            # شمارش تغییرات تب
            tab_change_count = tab_change.count_tab_changes()

            # ارسال هشدار فقط یک‌بار در صورت رسیدن به ۲۰ تغییر تب
            if tab_change_count >= 40:
                if not tab_change.last_warning_time or (now() - tab_change.last_warning_time) >= timedelta(minutes=5):
                    tab_change.last_warning_time = now()
                    tab_change.save()
                    return JsonResponse({'status': 'warning', 'message': 'شما ۲۰ بار از صفحه آزمون خارج شده اید.'})

            # محاسبه زمان کل دور بودن
            total_time_away = tab_change.calculate_total_time_away()
            print(f"Total time away: {total_time_away}")

            # ارسال هشدار برای زمان طولانی دور بودن
            current_time = now()
            if total_time_away >= timedelta(seconds=5):
                if not tab_change.last_warning_time or (current_time - tab_change.last_warning_time) >= timedelta(minutes=10):
                    tab_change.last_warning_time = current_time
                    tab_change.save()
                    return JsonResponse({'status': 'warning', 'message': 'شما برای مدت زیادی از صفحه آزمون خارج شده اید!'})

            return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)
