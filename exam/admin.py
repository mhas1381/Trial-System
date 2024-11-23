from django.contrib import admin
from .models import TabChange
from django.utils.safestring import mark_safe
import json

class TabChangeAdmin(admin.ModelAdmin):
    list_display = ('user', 'updated_at', 'formatted_tab_changes')
    readonly_fields = ('formatted_tab_changes',)  # نمایش فیلد به صورت فقط‌خواندنی

    def formatted_tab_changes(self, obj):
        # فرمت داده‌ها برای نمایش بهتر در پنل ادمین
        try:
            formatted_json = json.dumps(obj.tab_changes, indent=4)
            return mark_safe(f'<pre>{formatted_json}</pre>')  # نمایش با قالب <pre> برای بهتر دیدن JSON
        except Exception as e:
            return "Invalid JSON Format"

    formatted_tab_changes.short_description = "Tab Changes"  # نام ستون در پنل ادمین

admin.site.register(TabChange, TabChangeAdmin)
