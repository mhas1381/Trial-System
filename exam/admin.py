from django.contrib import admin
from .models import TabChange

class TabChangeAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp', 'ip_address')  # نمایش نام کاربر، نوع تغییر، زمان و IP
    list_filter = ('action', 'timestamp', 'user')  # فیلتر بر اساس نوع تغییر، زمان و کاربر
    search_fields = ('user__username', 'action')  # جستجو بر اساس نام کاربر و نوع تغییر
    ordering = ('-timestamp',)  # ترتیب نمایش بر اساس زمان به ترتیب نزولی

admin.site.register(TabChange, TabChangeAdmin)
