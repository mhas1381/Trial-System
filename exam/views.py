from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
import json
from .models import TabChange
# Create your views here.
def exam_view(request):

    return render(request , "exam/exam.html")

@csrf_exempt
def track_tab_change(request):
    """ذخیره تغییرات تب در دیتابیس"""
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        ip_address = request.META.get('REMOTE_ADDR')
        user = request.user  # گرفتن کاربر لاگین شده

        if action in ['tab-hidden', 'tab-visible']:
            TabChange.objects.create(
                user=user,  # ذخیره تغییرات برای کاربر
                user_agent=user_agent,
                action=action,
                ip_address=ip_address,
                timestamp=now()
            )
        print("User changed tab!")
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
