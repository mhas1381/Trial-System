from django.contrib import admin
from .models import TabChange,AudioRecording
from django.utils.safestring import mark_safe
import json

class TabChangeAdmin(admin.ModelAdmin):
    list_display = ('user', 'updated_at', 'formatted_tab_changes')
    readonly_fields = ('formatted_tab_changes',) 
    def formatted_tab_changes(self, obj):
        try:
            formatted_json = json.dumps(obj.tab_changes, indent=4)
            return mark_safe(f'<pre>{formatted_json}</pre>')  
        except Exception as e:
            return "Invalid JSON Format"

    formatted_tab_changes.short_description = "Tab Changes"  

admin.site.register(TabChange, TabChangeAdmin)

@admin.register(AudioRecording)
class AudioRecordingAdmin(admin.ModelAdmin):
    list_display = ('user', 'file_name', 'created_at')  
    list_filter = ('created_at',)  
    search_fields = ('user__phone_number',)  
    def file_name(self, obj):
        return obj.file.name.split('/')[-1]  
    file_name.short_description = 'File Name'  